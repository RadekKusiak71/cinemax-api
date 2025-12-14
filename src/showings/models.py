from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from core.models import Language
from movies.models import Movie
from showings.utils import get_overlapping_screenings
from theaters.models import TheaterHall


class ShowingFormat(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class ShowingVariant(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='showing_variants')
    format = models.ForeignKey(ShowingFormat, on_delete=models.PROTECT, related_name='showing_variants')
    subtitles = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    dubbing = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='+', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['movie', 'format', 'subtitles', 'dubbing'],
                name='unique_showing_variant',
                violation_error_message='A showing variant with this combination of movie, format, subtitles, and dubbing already exists.',
                violation_error_code='unique_showing_variant_violation',
                nulls_distinct=False,
            ),
            models.CheckConstraint(
                condition=~models.Q(dubbing__isnull=False, subtitles__isnull=False),
                name='no_dubbing_and_subtitles_simultaneously',
                violation_error_message='A movie variant cannot have both dubbing and subtitles simultaneously.',
                violation_error_code='no_dubbing_and_subtitles_simultaneously_violation'
            )
        ]

    def __str__(self) -> str:
        base_str: str = f'{self.format.name}'

        if self.dubbing:
            base_str += f' Dubbing {self.dubbing.name}'
        if self.subtitles:
            base_str += f' Subtitles {self.subtitles.name}'

        if not self.dubbing and not self.subtitles:
            base_str += f' Original {self.movie.original_language.name}'

        return base_str
    
class Showing(models.Model):
    CLEANUP_BUFFER_MINUTES = 15

    theater_hall = models.ForeignKey(TheaterHall, on_delete=models.PROTECT, related_name='showings')
    variant = models.ForeignKey(ShowingVariant, on_delete=models.PROTECT, related_name='showings')
    start_time = models.DateTimeField()
    ticket_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        help_text='Price in EUR', 
        validators=[
            MinValueValidator(0.0, message='Price must be a non-negative value.')
        ]
    )

    def __str__(self) -> str:
        return f'{self.variant.movie.title} - {self.start_time} in {self.theater_hall.number}'
    
    def clean(self) -> None:
        super().clean()
        
        if self.theater_hall and self.start_time and self.variant:
            if get_overlapping_screenings(
                theater_hall_id=self.theater_hall.id,
                screening_start=self.start_time,
                screening_end=self.start_time + timedelta(minutes=self.CLEANUP_BUFFER_MINUTES + self.variant.movie.duration),
            ).exclude(id=self.id).exists():
                raise ValidationError({
                    'start_time': 'This screening overlaps with an existing screening in the same hall.'
                })