import pytest
from django.urls import reverse
from django.utils import timezone

from showings.views import ListMovieShowingsAPIView

pytestmark = pytest.mark.django_db


def _get_url(movie_id: int) -> str:
    return reverse("movies:list-movie-showings", kwargs={"movie_id": movie_id})

def test_list_with_invalid_movie_id_returns_404(api_client):
    url = _get_url(9999)
    res = api_client.get(url)
    assert res.status_code == 404
    data = res.json()
    assert data["detail"] == "No Movie matches the given query."

def test_list_returns_only_showings_for_movie_and_date(
    api_client,
    movie_factory,
    showing_factory,
    showing_variant_factory,
):
    movie = movie_factory()
    other_movie = movie_factory()

    variant = showing_variant_factory(movie=movie)
    other_variant = showing_variant_factory(movie=other_movie)

    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    s1 = showing_factory(variant=variant, start_time=timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time())))
    s2 = showing_factory(variant=variant, start_time=timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time())))

    showing_factory(variant=other_variant, start_time=timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time())))

    showing_factory(variant=variant, start_time=timezone.make_aware(timezone.datetime.combine(tomorrow, timezone.datetime.min.time())))

    url = _get_url(movie.id)
    res = api_client.get(url, {"date": str(today)})

    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1

    group = data[0]
    assert "variant_key" in group
    assert "showings" in group
    assert len(group["showings"]) == 2

    returned_ids = {x["id"] for x in group["showings"]}
    assert returned_ids == {s1.id, s2.id}


def test_list_groups_by_variant_key(
    api_client,
    movie_factory,
    showing_factory,
    showing_variant_factory,
):
    movie = movie_factory()
    v1 = showing_variant_factory(movie=movie)
    v2 = showing_variant_factory(movie=movie)

    today = timezone.now().date()
    dt = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))

    s1 = showing_factory(variant=v1, start_time=dt)
    s2 = showing_factory(variant=v1, start_time=dt)
    s3 = showing_factory(variant=v2, start_time=dt)

    url = _get_url(movie.id)
    res = api_client.get(url, {"date": str(today)})

    assert res.status_code == 200
    data = res.json()

    assert len(data) == 2

    groups = {g["variant_key"]: g["showings"] for g in data}

    assert str(v1) in groups
    assert str(v2) in groups

    assert {x["id"] for x in groups[str(v1)]} == {s1.id, s2.id}
    assert {x["id"] for x in groups[str(v2)]} == {s3.id}


def test_list_default_date_is_today(
    api_client,
    movie_factory,
    showing_factory,
    showing_variant_factory,
):
    movie = movie_factory()
    variant = showing_variant_factory(movie=movie)

    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    dt_today = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    dt_tomorrow = timezone.make_aware(timezone.datetime.combine(tomorrow, timezone.datetime.min.time()))

    s_today = showing_factory(variant=variant, start_time=dt_today)
    showing_factory(variant=variant, start_time=dt_tomorrow)

    url = _get_url(movie.id)
    res = api_client.get(url)

    assert res.status_code == 200
    data = res.json()

    assert len(data) == 1
    returned_ids = {x["id"] for x in data[0]["showings"]}
    assert returned_ids == {s_today.id}


def test_group_showings_by_variant_unit(
    showing_factory,
    showing_variant_factory,
):
    v1 = showing_variant_factory()
    v2 = showing_variant_factory()

    dt = timezone.now()
    s1 = showing_factory(variant=v1, start_time=dt)
    s2 = showing_factory(variant=v1, start_time=dt)
    s3 = showing_factory(variant=v2, start_time=dt)

    view = ListMovieShowingsAPIView()
    grouped = view.group_showings_by_variant([s1, s2, s3])

    assert isinstance(grouped, list)
    assert len(grouped) == 2

    groups = {g["variant_key"]: g["showings"] for g in grouped}
    assert {x.id for x in groups[str(v1)]} == {s1.id, s2.id}
    assert {x.id for x in groups[str(v2)]} == {s3.id}
