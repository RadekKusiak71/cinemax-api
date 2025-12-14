import pytest

from payments.exceptions import InvalidBookingStatusError
from payments.events import CheckoutExpiredStrategy
from reservations.models import ReservationStatus, Ticket

pytestmark = pytest.mark.django_db

def test_handle_cancels_booking_and_deletes_tickets(reservation_factory, ticket_factory):
    reservation = reservation_factory(status=ReservationStatus.PENDING)

    ticket_factory(reservation=reservation)
    ticket_factory(reservation=reservation)

    assert Ticket.objects.filter(reservation=reservation).count() == 2

    strategy = CheckoutExpiredStrategy()
    event = {
        'data': {
            'object': {
                'metadata': {'reservation_id': str(reservation.id)}
            }
        }
    }

    strategy.handle(event)

    reservation.refresh_from_db()
    assert reservation.status == ReservationStatus.CANCELLED
    assert Ticket.objects.filter(reservation=reservation).count() == 0


def test_handle_ignores_non_pending_booking(reservation_factory, ticket_factory):
    reservation = reservation_factory(status=ReservationStatus.CONFIRMED)
    ticket_factory(reservation=reservation)

    strategy = CheckoutExpiredStrategy()
    event = {'data': {'object': {'metadata': {'reservation_id': str(reservation.id)}}}}

    with pytest.raises(InvalidBookingStatusError):
        strategy.handle(event)

    reservation.refresh_from_db()
    assert reservation.status == ReservationStatus.CONFIRMED
    assert Ticket.objects.filter(reservation=reservation).exists()