import pytest

from reservations import exceptions as exc
from reservations.models import ReservationStatus, Ticket
from reservations.services import cancel_reservation

pytestmark = pytest.mark.django_db


def test_cancel_reservation_sets_status_cancelled_and_deletes_tickets(
    reservation_factory,
    ticket_factory,
    seat_factory,
    theater_hall_factory,
    showing_factory,
    user_factory,
):
    user = user_factory()
    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall)

    reservation = reservation_factory(user=user, showing=showing, status=ReservationStatus.PENDING)

    seat1 = seat_factory(theater_hall=hall)
    seat2 = seat_factory(theater_hall=hall)

    ticket_factory(reservation=reservation, seat=seat1)
    ticket_factory(reservation=reservation, seat=seat2)

    assert Ticket.objects.filter(reservation=reservation).count() == 2

    cancel_reservation(reservation)

    reservation.refresh_from_db()
    assert reservation.status == ReservationStatus.CANCELLED
    assert Ticket.objects.filter(reservation=reservation).count() == 0


@pytest.mark.parametrize(
    "status",
    [ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED, ReservationStatus.EXPIRED],
)
def test_cancel_reservation_raises_if_status_not_pending(
    reservation_factory,
    status,
):
    reservation = reservation_factory(status=status)

    with pytest.raises(exc.InvalidReservationStatusException):
        cancel_reservation(reservation)
