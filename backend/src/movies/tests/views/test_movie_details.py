from collections.abc import Callable

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from movies.models import Movie

pytestmark = pytest.mark.django_db

@pytest.fixture
def movie_details(api_client: APIClient) -> Callable:
    def _request(movie_id: int) -> None:
        return api_client.get(reverse("movies:movie-detail", args=[movie_id]))
    return _request

def test_movie_details_success(movie_details: Callable, movie: Movie) -> None:
    response = movie_details(movie.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == movie.id
    assert response.data['original_language'] == movie.original_language.name
    assert 'title' in response.data
    assert 'summary' in response.data
    assert 'release_year' in response.data
    assert 'poster_image' in response.data
    assert 'duration' in response.data
    assert 'age_restriction' in response.data
    assert 'genres' in response.data
    assert 'director' in response.data

def test_movie_details_without_authentication(api_client: APIClient, movie_details: Callable, movie: Movie) -> None:
    api_client.force_authenticate(user=None)
    response = movie_details(movie_id=movie.id)
    assert response.status_code == status.HTTP_200_OK

def test_movie_details_not_found(movie_details: Callable) -> None:
    response = movie_details(movie_id=9999)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"detail": "No Movie matches the given query."}