from logging import getLogger

from celery import shared_task
from django.utils import timezone

from reservations.models import Reservation, ReservationStatus, Ticket

logger = getLogger(__name__)

@shared_task
def cancel_expired_reservations() -> None:
    """ Mark reservations as expired if they have not been confirmed within the allowed time frame (Tickets are deleted with models.CASCADE). """
    logger.info("Starting task to cancel expired reservations.")

    reservation_ids_to_expire: list[int] = Reservation.objects.filter(
        status=ReservationStatus.PENDING,
        created_at__lt=timezone.now() - Reservation.EXPIRATION_DELTA,
    ).values_list('id', flat=True)

    if not reservation_ids_to_expire:
        logger.info("No expired reservations found.")
        return
    
    Ticket.objects.filter(reservation_id__in=reservation_ids_to_expire).delete()

    updated_count: int = Reservation.objects.filter(
        id__in=reservation_ids_to_expire
    ).update(status=ReservationStatus.EXPIRED)

    logger.info(f"Expired {updated_count} reservations.")

    