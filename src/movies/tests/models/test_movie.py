import pytest
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError

from movies.models import Movie

pytestmark = pytest.mark.django_db


def test_movie_str_repr(movie: Movie) -> None:
    assert str(movie) == f"{movie.title} ({movie.release_year})"

def test_movie_age_restriction_min_value_validation(movie: Movie) -> None:
    movie.age_restriction = -1
    with pytest.raises(ValidationError) as exc_info:
        movie.full_clean()
    
    assert 'age_restriction' in exc_info.value.message_dict
    assert exc_info.value.message_dict['age_restriction'] == ['Ensure this value is greater than or equal to 0.']

def test_movie_age_restriction_max_value_validation(movie: Movie) -> None:
    movie.age_restriction = 22
    with pytest.raises(ValidationError) as exc_info:
        movie.full_clean()
    
    assert 'age_restriction' in exc_info.value.message_dict
    assert exc_info.value.message_dict['age_restriction'] == ['Ensure this value is less than or equal to 21.']

def test_movie_release_year_min_value_validation(movie: Movie) -> None:
    movie.release_year = 1799
    with pytest.raises(ValidationError) as exc_info:
        movie.full_clean()
    
    assert 'release_year' in exc_info.value.message_dict
    assert exc_info.value.message_dict['release_year'] == ['Ensure this value is greater than or equal to 1800.']

def test_movie_is_protected_due_to_director_deletion(movie: Movie, director) -> None:
    with pytest.raises(ProtectedError):
        director.delete()

def test_movie_is_protected_due_to_original_language_deletion(movie: Movie, language) -> None:
    with pytest.raises(ProtectedError):
        language.delete()

def test_movie_duration_min_value_validation(movie: Movie) -> None:
    movie.duration = 0
    with pytest.raises(ValidationError) as exc_info:
        movie.full_clean()
    
    assert 'duration' in exc_info.value.message_dict
    assert exc_info.value.message_dict['duration'] == ['Duration must be at least 1 minute.']

def test_movie_duration_max_value_validation(movie: Movie) -> None:
    movie.duration = 501
    with pytest.raises(ValidationError) as exc_info:
        movie.full_clean()
    
    assert 'duration' in exc_info.value.message_dict
    assert exc_info.value.message_dict['duration'] == ['Duration cannot exceed 500 minutes.']