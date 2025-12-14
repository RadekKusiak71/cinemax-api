from django.core.validators import MinValueValidator
from django.db import models

from showings.models import Showing
from theaters.models import Seat
from users.models import User
from datetime import timedelta

class ReservationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    EXPIRED = 'EXPIRED', 'Expired'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Reservation(models.Model):
    EXPIRATION_DELTA = timedelta(minutes=15)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    showing = models.ForeignKey(Showing, on_delete=models.PROTECT, related_name='reservations')
    full_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Total price for the reservation in EUR."
    )
    status = models.CharField(max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Reservation {self.id} by {self.user.email} for {self.showing.variant.movie.title}"
    
class Ticket(models.Model):

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT, related_name='tickets')
    price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Price for the ticket in EUR."
    )
    
    def __str__(self) -> str:
        return f"Ticket {self.id} for Reservation {self.reservation.id} - Seat {self.seat.row}-{self.seat.number}"
