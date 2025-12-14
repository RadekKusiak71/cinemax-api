from decimal import Decimal

import pytest

from reservations import exceptions as exc
from reservations.models import ReservationStatus, Ticket
from reservations.services import MAX_SEATS_PER_RESERVATION, create_reservation

pytestmark = pytest.mark.django_db


def test_create_reservation_creates_pending_reservation_and_tickets(
    user_factory,
    showing_factory,
    theater_hall_factory,
    seat_factory,
):
    user = user_factory()
    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall, ticket_price=Decimal("12.50"))

    seats = [
        seat_factory(theater_hall=hall),
        seat_factory(theater_hall=hall),
        seat_factory(theater_hall=hall),
    ]
    seat_ids = [s.id for s in seats]

    reservation = create_reservation(user=user, showing=showing, seat_ids=seat_ids)

    reservation.refresh_from_db()

    assert reservation.user_id == user.id
    assert reservation.showing_id == showing.id
    assert reservation.status == ReservationStatus.PENDING
    assert reservation.full_price == showing.ticket_price * Decimal(len(seats))

    tickets = Ticket.objects.filter(reservation=reservation).order_by("id")
    assert tickets.count() == len(seats)

    ticket_seat_ids = {t.seat_id for t in tickets}
    assert ticket_seat_ids == set(seat_ids)

    assert all(t.price == showing.ticket_price for t in tickets)


def test_create_reservation_raises_if_existing_pending_reservation(
    user_factory,
    showing_factory,
    reservation_factory,
):
    user = user_factory()
    showing = showing_factory()

    reservation_factory(user=user, showing=showing, status=ReservationStatus.PENDING)

    with pytest.raises(exc.ExistingPendingReservationException):
        create_reservation(user=user, showing=showing, seat_ids=[1])


def test_create_reservation_raises_if_too_many_seats(
    user_factory,
    showing_factory,
):
    user = user_factory()
    showing = showing_factory()

    seat_ids = list(range(1, MAX_SEATS_PER_RESERVATION + 2))  # 7

    with pytest.raises(exc.MaxSeatsPerReservationExceededException):
        create_reservation(user=user, showing=showing, seat_ids=seat_ids)


def test_create_reservation_raises_if_any_seat_not_in_showing_hall(
    user_factory,
    showing_factory,
    theater_hall_factory,
    seat_factory,
):
    user = user_factory()

    hall_a = theater_hall_factory()
    hall_b = theater_hall_factory()

    showing = showing_factory(theater_hall=hall_a)

    seat_ok = seat_factory(theater_hall=hall_a)
    seat_wrong_hall = seat_factory(theater_hall=hall_b)

    with pytest.raises(exc.SeatDoesNotExistException):
        create_reservation(
            user=user,
            showing=showing,
            seat_ids=[seat_ok.id, seat_wrong_hall.id],
        )


def test_create_reservation_raises_if_seat_already_booked_pending(
    user_factory,
    showing_factory,
    theater_hall_factory,
    seat_factory,
    reservation_factory,
    ticket_factory,
):
    user = user_factory()
    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall)

    seat1 = seat_factory(theater_hall=hall)
    seat2 = seat_factory(theater_hall=hall)

    other_user = user_factory()
    existing_reservation = reservation_factory(
        user=other_user,
        showing=showing,
        status=ReservationStatus.PENDING,
    )
    ticket_factory(reservation=existing_reservation, seat=seat1)

    with pytest.raises(exc.SeatsAlreadyBookedException):
        create_reservation(user=user, showing=showing, seat_ids=[seat1.id, seat2.id])


def test_create_reservation_raises_if_seat_already_booked_confirmed(
    user_factory,
    showing_factory,
    theater_hall_factory,
    seat_factory,
    reservation_factory,
    ticket_factory,
):
    user = user_factory()
    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall)

    seat1 = seat_factory(theater_hall=hall)

    other_user = user_factory()
    existing_reservation = reservation_factory(
        user=other_user,
        showing=showing,
        status=ReservationStatus.CONFIRMED,
    )
    ticket_factory(reservation=existing_reservation, seat=seat1)

    with pytest.raises(exc.SeatsAlreadyBookedException):
        create_reservation(user=user, showing=showing, seat_ids=[seat1.id])
