from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

pytestmark = pytest.mark.django_db


def _get_url(showing_id: int) -> str:
    return reverse("showings:showing-detail", kwargs={"pk": showing_id})


def test_retrieve_showing_returns_404_when_not_found(api_client):
    url = _get_url(999999999)
    res = api_client.get(url)

    assert res.status_code == 404
    assert res.json()["detail"] == "No Showing matches the given query."


def test_retrieve_showing_returns_details_with_calculated_end_time(
    api_client,
    movie_factory,
    showing_variant_factory,
    theater_hall_factory,
    showing_factory,
):
    hall = theater_hall_factory(number=7)

    movie = movie_factory(duration=120)

    variant = showing_variant_factory(movie=movie)

    start_time = timezone.now().replace(microsecond=0)

    showing = showing_factory(
        variant=variant,
        theater_hall=hall,
        start_time=start_time,
    )

    url = _get_url(showing.id)
    res = api_client.get(url)

    assert res.status_code == 200
    data = res.json()

    assert data["id"] == showing.id
    assert "start_time" in data
    assert "end_time" in data
    assert data["theater_hall"] == str(hall.number)
    assert data["variant"] == str(variant)
    assert isinstance(data["movie"], dict)

    cleanup = getattr(showing, "CLEANUP_BUFFER_MINUTES")
    expected_end = start_time + timedelta(minutes=movie.duration + cleanup)

    returned_end = timezone.datetime.fromisoformat(data["end_time"])
    if timezone.is_naive(returned_end):
        returned_end = timezone.make_aware(returned_end)

    assert returned_end == expected_end


def test_retrieve_showing_includes_movie_details_structure(
    api_client,
    movie_factory,
    showing_variant_factory,
    theater_hall_factory,
    showing_factory,
):
    hall = theater_hall_factory(number=1)
    movie = movie_factory()
    variant = showing_variant_factory(movie=movie)
    showing = showing_factory(variant=variant, theater_hall=hall)

    url = _get_url(showing.id)
    res = api_client.get(url)

    assert res.status_code == 200
    data = res.json()

    assert isinstance(data["movie"], dict)
    assert "id" in data["movie"]
    assert data["movie"]["id"] == movie.id
