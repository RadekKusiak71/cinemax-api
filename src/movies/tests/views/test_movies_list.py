from collections.abc import Callable
from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from movies.factories import MovieFactory
from movies.models import Movie
from showings.factories import ShowingFactory, ShowingVariantFactory
from showings.models import Showing, ShowingVariant
from theaters.factories import TheaterHallFactory
from theaters.models import TheaterHall

pytestmark = pytest.mark.django_db

@pytest.fixture
def list_movies(api_client: APIClient) -> Callable:
    def _request(**kwargs):
        return api_client.get("/api/movies/", kwargs)
    return _request

def test_list_movies_success(
    list_movies: Callable,
    movie: Movie,
    showing_factory: ShowingFactory,
) -> None:

    showing_factory.create(variant__movie=movie, start_time=timezone.now() + timedelta(days=1))

    response = list_movies()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert len(response.data["results"]) == 1

    movie_data: dict = response.data["results"][0]
    assert "id" in movie_data
    assert "title" in movie_data
    assert "poster_image" in movie_data
    assert "release_year" in movie_data

def test_list_movies_returns_movies_with_scheduled_screenings_only(
    list_movies: Callable, 
    movie: Movie,
    showing_factory: ShowingFactory,
) -> None:
    Showing.objects.filter(
        start_time__gt=timezone.now()
    ).delete()

    showing_factory.create(variant__movie=movie, start_time=timezone.now() - timedelta(days=1))

    response = list_movies()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert len(response.data["results"]) == 0

def test_list_movies_ordering(
    list_movies: Callable, 
    movie: Movie,
    movie_factory: MovieFactory,
    showing_factory: ShowingFactory,
) -> None:
    
    movie2: Movie = movie_factory.create(title="A Movie")

    showing_movie1: Showing = showing_factory.create(variant__movie=movie, start_time=timezone.now() + timedelta(days=2))
    showing_movie2: Showing = showing_factory.create(variant__movie=movie2, start_time=timezone.now() + timedelta(days=1))

    response = list_movies()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert len(response.data["results"]) == 2

    first_movie_data: dict = response.data["results"][0]
    second_movie_data: dict = response.data["results"][1]
    assert first_movie_data["id"] == showing_movie2.variant.movie.id
    assert second_movie_data["id"] == showing_movie1.variant.movie.id

def test_list_movie_without_authentication(
    api_client: APIClient, 
    list_movies: Callable,
    movie: Movie,
    showing_factory: ShowingFactory,
) -> None:
    api_client.force_authenticate(user=None)
    showing_factory.create(variant__movie=movie, start_time=timezone.now() + timedelta(days=1))

    response = list_movies()
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, dict)
    assert len(response.data["results"]) == 1
