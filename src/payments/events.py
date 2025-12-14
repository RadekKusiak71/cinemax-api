import logging
from abc import ABC, abstractmethod

from django.db import transaction
from stripe import Event

from payments.exceptions import InvalidBookingStatusError
from reservations.models import Reservation, ReservationStatus, Ticket

logger = logging.getLogger(__name__)

class StripeEventStrategy(ABC):
    def extract_event_data(self, event: Event) -> dict:
        return event.get('data', {}).get('object', {})

    @abstractmethod
    def handle(self, event: Event) -> None:
        pass

class CheckoutCompletedStrategy(StripeEventStrategy):

    def handle(self, event: Event) -> None:
        event_data: dict = self.extract_event_data(event)
        reservation_id: str | None = event_data.get("metadata", {}).get("reservation_id")
        if not reservation_id:
            logger.error(f"No `reservation_id` found in #{event_data.get('id')} checkout session")
            return

        try:
            reservation: Reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            logger.error(f'Reservation not found for ID: {reservation_id}')
            return

        if reservation.status != ReservationStatus.PENDING:
            logger.info(f'Reservation {reservation.id} already processed with status {reservation.status}.')
            raise InvalidBookingStatusError(f'Reservation {reservation.id} has invalid status {reservation.status} for confirmation.')

        reservation.status = ReservationStatus.CONFIRMED
        reservation.save()
        logger.info(f'Reservation {reservation.id} confirmed.')

class CheckoutExpiredStrategy(StripeEventStrategy):

    @transaction.atomic
    def handle(self, event: Event) -> None:
        event_data: dict = self.extract_event_data(event)
        reservation_id: str | None = event_data.get("metadata", {}).get("reservation_id")
        if not reservation_id:
            logger.error(f"No `reservation_id` found in #{event_data.get('id')} checkout session")
            return

        try:
            reservation: Reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            logger.error(f'Reservation not found for ID: {reservation_id}')
            return

        if reservation.status != ReservationStatus.PENDING:
            logger.info(f'Reservation {reservation.id} already processed with status {reservation.status}.')
            raise InvalidBookingStatusError(f'Reservation {reservation.id} has invalid status {reservation.status} for cancellation.')

        reservation.status = ReservationStatus.CANCELLED
        reservation.save()
        Ticket.objects.filter(reservation=reservation).delete()
        logger.info(f'Reservation {reservation.id} cancelled.')

class StripeWebhookService:
    strategies: dict[str, type[StripeEventStrategy]] = {
        'checkout.session.completed': CheckoutCompletedStrategy,
        'checkout.session.expired': CheckoutExpiredStrategy,
    }

    def choose_strategy(self, event: Event) -> type[StripeEventStrategy] | None:
        event_type: str = event.get('type')
        strategy_class: StripeEventStrategy | None = self.strategies.get(event_type)
        if not strategy_class:
            logger.warning(f"Unhandled event type: {event_type}")
            return None
        return strategy_class

    def process(self, event: Event) -> None:
        strategy_class: type[StripeEventStrategy] | None = self.choose_strategy(event)
        if not strategy_class:
            return
        strategy_class().handle(event)