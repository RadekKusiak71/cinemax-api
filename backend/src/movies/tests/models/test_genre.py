import pytest
from movies.models import Genre
from movies.factories import GenreFactory
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db

def test_genre_str_representation(genre: Genre) -> None:
    assert str(genre) == genre.name

def test_genre_name_uniqueness(genre: Genre, genre_factory: GenreFactory) -> None:
    with pytest.raises(ValidationError) as exc_info:
        new_genre: Genre = genre_factory.build(name=genre.name)
        new_genre.full_clean()

    assert 'name' in exc_info.value.message_dict
    assert exc_info.value.message_dict['name'] == ['Genre with this Name already exists.'] 