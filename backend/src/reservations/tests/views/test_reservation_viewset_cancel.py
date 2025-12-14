import pytest
from django.urls import reverse

from reservations.models import ReservationStatus, Ticket

pytestmark = pytest.mark.django_db


def _detail_url(reservation_id: int) -> str:
    return reverse("reservations:reservations-detail", kwargs={"booking_id": reservation_id})

def test_cancel_requires_auth(api_client, reservation_factory):
    reservation = reservation_factory(status=ReservationStatus.PENDING)

    res = api_client.delete(_detail_url(reservation.id))

    assert res.status_code == 401

def test_cancel_returns_404_when_not_found(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    res = api_client.delete(_detail_url(999999999))

    assert res.status_code == 404
    assert res.json()["detail"] == "No Reservation matches the given query."

def test_cancel_sets_status_cancelled_and_deletes_tickets(
    api_client,
    user_factory,
    reservation_factory,
    ticket_factory,
    seat_factory,
    showing_factory,
    theater_hall_factory,
):
    user = user_factory()
    api_client.force_authenticate(user=user)

    hall = theater_hall_factory()
    showing = showing_factory(theater_hall=hall)

    reservation = reservation_factory(
        user=user,
        showing=showing,
        status=ReservationStatus.PENDING,
    )

    seat1 = seat_factory(theater_hall=hall)
    seat2 = seat_factory(theater_hall=hall)

    ticket_factory(reservation=reservation, seat=seat1)
    ticket_factory(reservation=reservation, seat=seat2)

    assert Ticket.objects.filter(reservation=reservation).count() == 2

    res = api_client.delete(_detail_url(reservation.id))

    assert res.status_code == 204

    reservation.refresh_from_db()
    assert reservation.status == ReservationStatus.CANCELLED
    assert Ticket.objects.filter(reservation=reservation).count() == 0


@pytest.mark.parametrize(
    "status",
    [ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED, ReservationStatus.EXPIRED],
)
def test_cancel_returns_400_when_status_not_pending(
    api_client,
    user_factory,
    reservation_factory,
    status,
):
    user = user_factory()
    api_client.force_authenticate(user=user)

    reservation = reservation_factory(user=user, status=status)

    res = api_client.delete(_detail_url(reservation.id))

    assert res.status_code == 400
    assert "detail" in res.json()
