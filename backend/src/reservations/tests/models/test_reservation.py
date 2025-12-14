import pytest
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from reservations.models import Reservation, ReservationStatus

pytestmark = pytest.mark.django_db

def test_reservation_str_repr(reservation: Reservation) -> None:
    assert str(reservation) == f"Reservation {reservation.id} by {reservation.user.email} for {reservation.showing.variant.movie.title}"

def test_reservation_full_price_min_value_validator(reservation: Reservation) -> None:
    with pytest.raises(ValidationError) as exc_info:
        reservation.full_price = -10.0
        reservation.full_clean()
    
    assert 'full_price' in exc_info.value.message_dict
    assert exc_info.value.message_dict['full_price'] == ['Ensure this value is greater than or equal to 0.0.']

def test_reservation_status_by_default(reservation: Reservation) -> None:
    assert reservation.status == ReservationStatus.PENDING

def test_reservation_is_protected_on_showing_delete(reservation: Reservation) -> None:
    with pytest.raises(ProtectedError):
        reservation.showing.delete()