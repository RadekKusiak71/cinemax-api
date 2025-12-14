import pytest
from django.core.exceptions import ValidationError
from django.db import models

from showings.factories import ShowingFormatFactory
from showings.models import ShowingFormat

pytestmark = pytest.mark.django_db


def test_showing_format_str(showing_format: ShowingFormat) -> None:
    assert str(showing_format) == showing_format.name

def test_showing_format_name_uniqueness(showing_format: ShowingFormat, showing_format_factory: ShowingFormatFactory) -> None:
    with pytest.raises(ValidationError) as exc_info:
        duplicate_format = showing_format_factory.build(name=showing_format.name)
        duplicate_format.full_clean()

    errors = exc_info.value.message_dict
    assert 'name' in errors
    assert errors['name'] == ['Showing format with this Name already exists.']