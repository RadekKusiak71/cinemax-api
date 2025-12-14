import pytest
from django.core.exceptions import ValidationError
from theaters.models import Seat
from theaters.factories import SeatFactory, TheaterHall

pytestmark = pytest.mark.django_db

def test_seat_str_representation(seat: Seat) -> None:
    expected_str = f"Hall {seat.theater_hall.number} - Row {seat.row}, Seat {seat.number}"
    assert str(seat) == expected_str

def test_unique_seat_row_and_number_within_theater_hall(seat_factory: SeatFactory, seat: Seat) -> None:
    with pytest.raises(ValidationError) as exc_info:
        seat2 = seat_factory.build(theater_hall=seat.theater_hall, row=seat.row, number=seat.number)
        seat2.full_clean()

    assert '__all__' in exc_info.value.message_dict
    assert "A seat with this row and number already exists in the specified theater hall." in exc_info.value.message_dict['__all__']


def test_seat_row_min_value_validation(seat_factory: SeatFactory) -> None:
    seat = seat_factory.build(row=0)
    with pytest.raises(ValidationError) as exc_info:
        seat.full_clean()

    assert 'row' in exc_info.value.message_dict
    assert "Ensure this value is greater than or equal to 1." in exc_info.value.message_dict['row']

def test_seat_number_min_value_validation(seat_factory: SeatFactory) -> None:
    seat = seat_factory.build(number=0)
    with pytest.raises(ValidationError) as exc_info:
        seat.full_clean()

    assert 'number' in exc_info.value.message_dict
    assert "Ensure this value is greater than or equal to 1." in exc_info.value.message_dict['number']