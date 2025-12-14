from django.core.exceptions import ValidationError
import pytest
from django.db.models import ProtectedError

from reservations.models import Ticket

pytestmark = pytest.mark.django_db

def test_ticket_string_repr(ticket: Ticket):
    assert str(ticket) == f"Ticket {ticket.id} for Reservation {ticket.reservation.id} - Seat {ticket.seat.row}-{ticket.seat.number}"

def test_ticket_is_protected_on_seat_delete(ticket: Ticket):
    with pytest.raises(ProtectedError):
        ticket.seat.delete()

def test_ticket_price_min_value(ticket: Ticket):
    ticket.price = -5.00
    with pytest.raises(ValidationError) as exc_info:
        ticket.full_clean()
    
    assert 'price' in exc_info.value.message_dict
    assert 'Ensure this value is greater than or equal to 0.0.' in exc_info.value.message_dict['price']
