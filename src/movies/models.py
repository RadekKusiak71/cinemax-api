import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import Language


def poster_image_upload_path(instance: type['Movie'], filename: str) -> str:
    ext = os.path.splitext(filename)[1]    
    return f'posters/{uuid.uuid4()}{ext}'

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    
class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Movie(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1500)
    release_year = models.PositiveIntegerField(validators=[MinValueValidator(1800)])
    poster_image = models.ImageField(upload_to=poster_image_upload_path)
    duration = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Duration must be at least 1 minute.'),
            MaxValueValidator(500, message='Duration cannot exceed 500 minutes.')
        ],
        help_text='Duration of movie in minutes'
    )
    age_restriction = models.PositiveIntegerField(
        default=0, 
        validators=[MaxValueValidator(21)],
        help_text="Age restriction in years (0 means suitable for all ages)."
    )
    original_language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='original_movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name='movies')

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"
