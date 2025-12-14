import pytest
from django.urls import reverse

from payments.exceptions import InvalidBookingStatusError
from reservations.models import ReservationStatus

pytestmark = pytest.mark.django_db


def _url(booking_id: int) -> str:
    return reverse("payments:reservation-checkout", kwargs={"booking_id": booking_id})


def test_checkout_requires_auth(api_client, reservation_factory):
    reservation = reservation_factory(status=ReservationStatus.PENDING)

    res = api_client.post(_url(reservation.id), format="json")

    assert res.status_code == 401


def test_checkout_returns_404_when_reservation_not_found(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    res = api_client.post(_url(999999999), format="json")

    assert res.status_code == 404
    assert res.json()["detail"] == "No Reservation matches the given query."


def test_checkout_returns_404_when_reservation_belongs_to_other_user(
    api_client,
    user_factory,
    reservation_factory,
):
    user = user_factory()
    other_user = user_factory()

    reservation = reservation_factory(
        user=other_user,
        status=ReservationStatus.PENDING,
    )

    api_client.force_authenticate(user=user)

    res = api_client.post(_url(reservation.id), format="json")

    assert res.status_code == 404
    assert res.json()["detail"] == "No Reservation matches the given query."


def test_checkout_returns_400_when_invalid_booking_status(
    api_client,
    user_factory,
    reservation_factory,
    mocker,
):
    user = user_factory()
    reservation = reservation_factory(user=user, status=ReservationStatus.CONFIRMED)

    api_client.force_authenticate(user=user)

    mocker.patch(
        "payments.views.create_checkout",
        side_effect=InvalidBookingStatusError("Cannot checkout reservation X: Status is CONFIRMED"),
    )

    res = api_client.post(_url(reservation.id), format="json")

    assert res.status_code == 400
    body = res.json()
    assert "detail" in body
    assert "status" in body["detail"].lower() or "cannot checkout" in body["detail"].lower()


def test_checkout_returns_201_with_session_id_and_url(
    api_client,
    user_factory,
    reservation_factory,
    mocker,
):
    user = user_factory()
    reservation = reservation_factory(user=user, status=ReservationStatus.PENDING)

    api_client.force_authenticate(user=user)

    class FakeSession:
        id = "cs_test_123"
        url = "https://checkout.stripe.com/pay/cs_test_123"

    mocker.patch("payments.views.create_checkout", return_value=FakeSession())

    res = api_client.post(_url(reservation.id), format="json")

    assert res.status_code == 201
    data = res.json()
    assert data["session_id"] == "cs_test_123"
    assert data["url"] == "https://checkout.stripe.com/pay/cs_test_123"
