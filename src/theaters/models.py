from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class TheaterHall(models.Model):
    number = models.CharField(
        max_length=30, 
        unique=True, 
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9 ]+$', 
                message="Theater hall number must contain only letters, numbers, and spaces.",
            ),
        ],
        help_text="Name of the theater hall (e.g., 'Hall 1', 'Hall 2').",
    )

    def __str__(self) -> str:
        return self.number

class Seat(models.Model):

    theater_hall = models.ForeignKey(
        TheaterHall, 
        on_delete=models.CASCADE, 
        related_name='seats',
        help_text="The theater hall to which this seat belongs.",
    )
    row = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Row number of the seat (starting from 1).")
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Seat number within the row (starting from 1).")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['theater_hall', 'row', 'number'],
                name='unique_seat_per_hall',
                violation_error_message='A seat with this row and number already exists in the specified theater hall.',
                violation_error_code='unique_seat_per_hall_violation',
            )
        ]

    def __str__(self) -> str:
        return f"Hall {self.theater_hall.number} - Row {self.row}, Seat {self.number}"
