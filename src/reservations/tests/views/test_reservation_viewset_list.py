import pytest
from django.urls import reverse
from django.utils import timezone

from reservations.models import Reservation, ReservationStatus

pytestmark = pytest.mark.django_db


def _list_url() -> str:
    return reverse("reservations:reservations-list")

def _items(data):
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    return data


def test_list_requires_auth(api_client):
    res = api_client.get(_list_url())
    assert res.status_code == 401



def test_list_returns_only_confirmed_ordered_by_created_at_desc(
    api_client,
    user_factory,
    reservation_factory,
    showing_factory,
):
    user = user_factory()
    api_client.force_authenticate(user=user)

    showing = showing_factory()

    r_old = reservation_factory(user=user, showing=showing, status=ReservationStatus.CONFIRMED)
    r_mid = reservation_factory(user=user, showing=showing, status=ReservationStatus.PENDING)
    r_new = reservation_factory(user=user, showing=showing, status=ReservationStatus.CONFIRMED)

    now = timezone.now()
    Reservation.objects.filter(pk=r_old.pk).update(created_at=now - timezone.timedelta(days=2))
    Reservation.objects.filter(pk=r_mid.pk).update(created_at=now - timezone.timedelta(days=1))
    Reservation.objects.filter(pk=r_new.pk).update(created_at=now)

    res = api_client.get(_list_url())

    assert res.status_code == 200
    data = res.json()
    items = _items(data)

    assert isinstance(items, list)

    returned_ids = [item["id"] for item in items]
    assert returned_ids == [r_new.id, r_old.id]

    first = items[0]
    assert "movie_id" in first
    assert "movie_title" in first
    assert "movie_duration" in first
    assert "showing_id" in first
    assert "showing_start_time" in first
    assert "theater_hall" in first
    assert "variant" in first

def test_list_returns_only_user_confirmed_reservations(
    api_client,
    user_factory,
    reservation_factory,
    showing_factory,
):
    user = user_factory()
    other = user_factory()
    api_client.force_authenticate(user=user)

    showing = showing_factory()

    mine = reservation_factory(user=user, showing=showing, status=ReservationStatus.CONFIRMED)
    reservation_factory(user=other, showing=showing, status=ReservationStatus.CONFIRMED)

    res = api_client.get(_list_url())

    assert res.status_code == 200
    data = res.json()
    items = _items(data)

    assert {x["id"] for x in items} == {mine.id}