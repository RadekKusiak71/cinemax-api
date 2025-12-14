from decimal import Decimal

from django.db import transaction
from django.db.models import Exists, OuterRef, QuerySet

from reservations import exceptions as exc
from reservations.models import Reservation, ReservationStatus, Ticket
from showings.models import Showing
from theaters.models import Seat
from users.models import User

MAX_SEATS_PER_RESERVATION = 6


@transaction.atomic
def create_reservation(user: User, showing: Showing, seat_ids: list[int]) -> Reservation:
    _assert_user_has_no_pending_reservation(user=user, showing=showing)

    seats: list[Seat] = validate_and_lock_seats(showing=showing, seat_ids=seat_ids)

    reservation: Reservation = Reservation(
        user=user,
        showing=showing,
        status=ReservationStatus.PENDING,
    )

    ticket_price: Decimal = showing.ticket_price
    reservation.full_price = ticket_price * Decimal(len(seats))

    reservation.save()

    Ticket.objects.bulk_create(
        [
            Ticket(seat=seat, price=ticket_price, reservation=reservation)
            for seat in seats
        ]
    )

    return reservation


def validate_and_lock_seats(showing: Showing, seat_ids: list[int]) -> list[Seat]:
    _validate_seat_ids(seat_ids)

    qs: QuerySet[Seat] = (
        Seat.objects
        .filter(id__in=seat_ids, theater_hall=showing.theater_hall)
        .annotate(
            is_reserved=Exists(
                Ticket.objects.filter(
                    reservation__showing=showing,
                    reservation__status__in=[ReservationStatus.CONFIRMED, ReservationStatus.PENDING],
                    seat_id=OuterRef("id"),
                )
            )
        )
        .select_for_update()
        .order_by("id")
    )

    seats = list(qs)

    if len(seats) != len(set(seat_ids)):
        raise exc.SeatDoesNotExistException()

    if any(seat.is_reserved for seat in seats):
        raise exc.SeatsAlreadyBookedException()

    return seats


def cancel_reservation(reservation: Reservation) -> None:
    if reservation.status != ReservationStatus.PENDING:
        raise exc.InvalidReservationStatusException("Only pending reservations can be canceled.")

    reservation.status = ReservationStatus.CANCELLED
    reservation.save(update_fields=["status"])

    Ticket.objects.filter(reservation=reservation).delete()


def _assert_user_has_no_pending_reservation(*, user: User, showing: Showing) -> None:
    exists: bool = Reservation.objects.filter(
        user=user,
        showing=showing,
        status=ReservationStatus.PENDING,
    ).exists()
    if exists:
        raise exc.ExistingPendingReservationException(
            "User already has a pending reservation for this showing."
        )


def _validate_seat_ids(seat_ids: list[int]) -> None:
    if not seat_ids:
        raise exc.SeatDoesNotExistException()

    if len(seat_ids) > MAX_SEATS_PER_RESERVATION:
        raise exc.MaxSeatsPerReservationExceededException()

    if len(set(seat_ids)) != len(seat_ids):
        raise exc.SeatsAlreadyBookedException("Duplicate seat IDs provided.")
