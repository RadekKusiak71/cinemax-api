from logging import getLogger

from celery import shared_task
from django.utils import timezone

from reservations.models import Reservation, ReservationStatus

logger = getLogger(__name__)

@shared_task
def cancel_expired_reservations() -> None:
    """ Mark reservations as expired if they have not been confirmed within the allowed time frame (Tickets are deleted with models.CASCADE). """
    logger.info("Starting task to cancel expired reservations.")

    updated_reservations_count: int = Reservation.objects.filter(
        status=ReservationStatus.PENDING,
        created_at__lt=timezone.now() - Reservation.EXPIRATION_DELTA,
    ).update(status=ReservationStatus.EXPIRED)

    logger.info(f"Expired {updated_reservations_count} expired reservations.")
