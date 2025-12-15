from decimal import Decimal

import pytest
from django.urls import reverse

from reservations.models import Reservation, ReservationStatus, Ticket

pytestmark = pytest.mark.django_db


def _create_url() -> str:
    return reverse("reservations:reservations-list")


def test_create_requires_auth(api_client, showing_factory, seat_factory, theater_hall_factory):
    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall)
    seat = seat_factory(theater_hall=hall)

    res = api_client.post(
        _create_url(),
        data={"showing_id": showing.id, "seat_ids": [seat.id]},
        format="json",
    )

    assert res.status_code == 401

def test_create_returns_404_when_showing_not_found(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    res = api_client.post(
        _create_url(),
        data={"showing_id": 999999999, "seat_ids": [1]},
        format="json",
    )

    assert res.status_code == 404
    assert res.json()["detail"] == "No Showing matches the given query."


def test_create_creates_reservation_and_returns_201(
    api_client,
    user_factory,
    showing_factory,
    theater_hall_factory,
    seat_factory,
):
    user = user_factory()
    api_client.force_authenticate(user=user)

    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall, ticket_price=Decimal("10.00"))

    seats = [
        seat_factory(theater_hall=hall),
        seat_factory(theater_hall=hall),
        seat_factory(theater_hall=hall),
    ]
    seat_ids = [s.id for s in seats]

    res = api_client.post(
        _create_url(),
        data={"showing_id": showing.id, "seat_ids": seat_ids},
        format="json",
    )

    assert res.status_code == 201
    data = res.json()

    assert "id" in data
    reservation_id = data["id"]

    reservation = Reservation.objects.get(pk=reservation_id)
    assert reservation.user_id == user.id
    assert reservation.showing_id == showing.id
    assert reservation.status == ReservationStatus.PENDING
    assert reservation.full_price == showing.ticket_price * Decimal(len(seat_ids))

    tickets = Ticket.objects.filter(reservation=reservation)
    assert tickets.count() == len(seat_ids)
    assert {t.seat_id for t in tickets} == set(seat_ids)
    assert all(t.price == showing.ticket_price for t in tickets)


def test_create_returns_400_when_user_already_has_more_than_3_pending_for_showing(
    api_client,
    user_factory,
    reservation_factory,
    showing_factory,
):
    user = user_factory()
    api_client.force_authenticate(user=user)

    showing = showing_factory()
    reservation_factory(user=user, showing=showing, status=ReservationStatus.PENDING)
    reservation_factory(user=user, showing=showing, status=ReservationStatus.PENDING)
    reservation_factory(user=user, showing=showing, status=ReservationStatus.PENDING)

    res = api_client.post(
        _create_url(),
        data={"showing_id": showing.id, "seat_ids": [1]},
        format="json",
    )

    assert res.status_code == 400
    body = res.json()
    assert "detail" in body
    assert "pending" in str(body["detail"]).lower()
