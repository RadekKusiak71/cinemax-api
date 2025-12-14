import pytest
from django.db.models import ProtectedError

from reservations.models import Ticket

pytestmark = pytest.mark.django_db

def test_ticket_string_repr(ticket: Ticket):
    assert str(ticket) == f"Ticket {ticket.id} for Reservation {ticket.reservation.id} - Seat {ticket.seat.row}-{ticket.seat.number}"

def test_ticket_is_protected_on_seat_delete(ticket: Ticket):
    with pytest.raises(ProtectedError):
        ticket.seat.delete()