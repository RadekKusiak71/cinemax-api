import pytest
from django.urls import reverse

from reservations.models import ReservationStatus

pytestmark = pytest.mark.django_db

def _get_url(showing_id: int) -> str:
    return reverse("showings:showing-room-layout", kwargs={"showing_id": showing_id})

def test_returns_404_when_showing_not_found(api_client):
    url = _get_url(999999999)
    res = api_client.get(url)

    assert res.status_code == 404
    assert res.json()["detail"] == "No Showing matches the given query."

def test_lists_all_seats_for_showing_hall_with_is_reserved_flag(
    api_client,
    theater_hall_factory,
    seat_factory,
    showing_factory,
    reservation_factory,
    ticket_factory,
):
    hall = theater_hall_factory()

    s1 = seat_factory(theater_hall=hall, row=2, number=5)
    s2 = seat_factory(theater_hall=hall, row=1, number=10)
    s3 = seat_factory(theater_hall=hall, row=1, number=2)

    showing = showing_factory(theater_hall=hall)

    r_pending = reservation_factory(showing=showing, status=ReservationStatus.PENDING)
    ticket_factory(reservation=r_pending, seat=s2)

    r_conf = reservation_factory(showing=showing, status=ReservationStatus.CONFIRMED)
    ticket_factory(reservation=r_conf, seat=s1)

    url = _get_url(showing.id)
    res = api_client.get(url)

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 3

    returned_order = [(x["row"], x["number"]) for x in data]
    assert returned_order == [(1, 2), (1, 10), (2, 5)]

    by_id = {x["id"]: x for x in data}
    assert by_id[s1.id]["is_reserved"] is True
    assert by_id[s2.id]["is_reserved"] is True
    assert by_id[s3.id]["is_reserved"] is False


def test_reserved_is_false_for_tickets_with_other_statuses(
    api_client,
    theater_hall_factory,
    seat_factory,
    showing_factory,
    reservation_factory,
    ticket_factory,
):
    hall = theater_hall_factory()
    seat = seat_factory(theater_hall=hall, row=1, number=1)
    showing = showing_factory(theater_hall=hall)

    r_cancelled = reservation_factory(showing=showing, status=ReservationStatus.CANCELLED)
    ticket_factory(reservation=r_cancelled, seat=seat)

    url = _get_url(showing.id)
    res = api_client.get(url)

    assert res.status_code == 200
    data = res.json()

    assert len(data) == 1
    assert data[0]["id"] == seat.id
    assert data[0]["is_reserved"] is False


def test_does_not_include_seats_from_other_halls(
    api_client,
    theater_hall_factory,
    seat_factory,
    showing_factory,
):
    hall1 = theater_hall_factory()
    hall2 = theater_hall_factory()

    seat1 = seat_factory(theater_hall=hall1, row=1, number=1)
    seat_factory(theater_hall=hall2, row=1, number=1)

    showing = showing_factory(theater_hall=hall1)

    url = _get_url(showing.id)
    res = api_client.get(url)

    assert res.status_code == 200
    data = res.json()

    assert {x["id"] for x in data} == {seat1.id}
