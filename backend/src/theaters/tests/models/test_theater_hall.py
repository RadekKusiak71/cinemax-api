import pytest
from django.core.exceptions import ValidationError

from theaters.factories import TheaterHallFactory
from theaters.models import TheaterHall

pytestmark = pytest.mark.django_db

def test_theater_hall_str_representation(theater_hall: TheaterHall) -> None:
    assert str(theater_hall) == theater_hall.number

@pytest.mark.parametrize(
    "invalid_number",
    [
        "Hall@1",
        "Hall#2",
        "Hall!3",
        "Hall$4",
        "Hall%5",
        "Hall^6",
        "Hall&7",
        "Hall*8",
        "Hall(9)",
    ],
)
def test_theater_hall_number_validation(theater_hall_factory: TheaterHallFactory, invalid_number: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        theater_hall = theater_hall_factory(number=invalid_number)
        theater_hall.full_clean()

    assert 'number' in exc_info.value.message_dict
    assert "Theater hall number must contain only letters, numbers, and spaces." in str(exc_info.value)
