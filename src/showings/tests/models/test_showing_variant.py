import pytest
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError

from core.models import Language
from movies.models import Movie
from showings.models import ShowingFormat, ShowingVariant

pytestmark = pytest.mark.django_db

def test_showing_variant_string_repr(showing_variant: ShowingVariant, language: Language) -> None:
    expected_str = f"{showing_variant.format.name} Original {showing_variant.movie.original_language.name}"
    assert str(showing_variant) == expected_str

    showing_variant.dubbing = language
    showing_variant.subtitles = None
    assert str(showing_variant) == f"{showing_variant.format.name} Dubbing {language.name}"

    showing_variant.dubbing = None
    showing_variant.subtitles = language
    assert str(showing_variant) == f"{showing_variant.format.name} Subtitles {language.name}"

def test_showing_variant_unique_constraint(showing_variant: ShowingVariant, showing_variant_factory: ShowingVariant) -> None:
    with pytest.raises(ValidationError) as exc_info:
        duplicate_variant = ShowingVariant(
            movie=showing_variant.movie,
            format=showing_variant.format,
            subtitles=showing_variant.subtitles,
            dubbing=showing_variant.dubbing
        )
        duplicate_variant.full_clean()

    assert 'A showing variant with this combination of movie, format, subtitles, and dubbing already exists.' in str(exc_info.value)

def test_creating_showing_variant_with_both_dubbing_and_subtitles_raises_validation_error(
    movie: Movie,
    showing_format: ShowingFormat,
    showing_variant_factory: ShowingVariant,
    language: Language,
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        variant = showing_variant_factory.build(
            movie=movie,
            format=showing_format,
            dubbing=language,
            subtitles=language
        )
        variant.full_clean()

    assert 'A movie variant cannot have both dubbing and subtitles simultaneously.' in str(exc_info.value)

def test_showing_variant_is_protected_from_subtitle_language_deletion(
    showing_variant: ShowingVariant,
    language: Language,
) -> None:
    showing_variant.subtitles = language
    showing_variant.save()
    with pytest.raises(ProtectedError):
        showing_variant.subtitles.delete()

def test_showing_variant_is_protected_from_dubbing_language_deletion(
    showing_variant: ShowingVariant,
    language: Language,
) -> None:
    showing_variant.dubbing = language
    showing_variant.save()
    with pytest.raises(ProtectedError):
        showing_variant.dubbing.delete()

def test_showing_variant_is_protected_from_movie_deletion(
    showing_variant: ShowingVariant,
) -> None:
    with pytest.raises(ProtectedError):
        showing_variant.movie.delete()

def test_showing_variant_is_protected_from_format_deletion(
    showing_variant: ShowingVariant,
) -> None:
    with pytest.raises(ProtectedError):
        showing_variant.format.delete()
