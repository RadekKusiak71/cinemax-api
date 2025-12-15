import pytest
from django.urls import reverse

from reservations.models import ReservationStatus, Ticket

pytestmark = pytest.mark.django_db


def _detail_url(booking_id: int) -> str:
    return reverse("reservations:reservations-detail", kwargs={"booking_id": booking_id})


def test_retrieve_requires_auth(api_client, reservation_factory):
    r = reservation_factory(status=ReservationStatus.CONFIRMED)
    res = api_client.get(_detail_url(r.id))
    assert res.status_code == 401

def test_retrieve_returns_404_for_other_users_reservation(
    api_client,
    user_factory,
    reservation_factory,
):
    user = user_factory()
    other = user_factory()
    api_client.force_authenticate(user=user)

    r = reservation_factory(user=other, status=ReservationStatus.CONFIRMED)

    res = api_client.get(_detail_url(r.id))

    assert res.status_code == 404
    assert res.json()["detail"] == "No Reservation matches the given query."


def test_retrieve_confirmed_includes_tickets_with_seat_info(
    api_client,
    user_factory,
    reservation_factory,
    ticket_factory,
    seat_factory,
    theater_hall_factory,
    showing_factory,
):
    user = user_factory()
    api_client.force_authenticate(user=user)

    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall)

    reservation = reservation_factory(
        user=user,
        showing=showing,
        status=ReservationStatus.CONFIRMED,
    )

    seat1 = seat_factory(theater_hall=hall, row=1, number=1)
    seat2 = seat_factory(theater_hall=hall, row=1, number=2)

    t1 = ticket_factory(reservation=reservation, seat=seat1)
    t2 = ticket_factory(reservation=reservation, seat=seat2)

    res = api_client.get(_detail_url(reservation.id))

    assert res.status_code == 200
    data = res.json()

    assert data["id"] == reservation.id
    assert data["status"] == ReservationStatus.CONFIRMED
    assert "movie_id" in data
    assert "movie_title" in data
    assert "movie_duration" in data
    assert "showing_id" in data
    assert "showing_start_time" in data
    assert "theater_hall" in data
    assert "variant" in data

    assert "tickets" in data
    assert isinstance(data["tickets"], list)
    assert len(data["tickets"]) == 2

    by_ticket_id = {x["id"]: x for x in data["tickets"]}
    assert by_ticket_id[t1.id]["seat_row"] == seat1.row
    assert by_ticket_id[t1.id]["seat_number"] == seat1.number
    assert by_ticket_id[t2.id]["seat_row"] == seat2.row
    assert by_ticket_id[t2.id]["seat_number"] == seat2.number

    assert "price" in by_ticket_id[t1.id]
    assert "price" in by_ticket_id[t2.id]
