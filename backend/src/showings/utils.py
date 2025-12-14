import typing
from datetime import datetime, timedelta

from django.db.models import (DateTimeField, DurationField, ExpressionWrapper,
                              F, QuerySet)

if typing.TYPE_CHECKING:
    from showings.models import Showing

def get_overlapping_screenings(
    theater_hall_id: int,
    screening_start: datetime,
    screening_end: datetime,
) -> QuerySet['Showing']:
    from showings.models import Showing

    return (
        Showing.objects.filter(
            theater_hall_id=theater_hall_id,
        )
        .annotate(
            movie_duration=ExpressionWrapper(
                (F('variant__movie__duration') + Showing.CLEANUP_BUFFER_MINUTES) * timedelta(minutes=1),
                output_field=DurationField()
            )
        )
        .annotate(
            end_time=ExpressionWrapper(
                F("start_time") + F('movie_duration'),
                output_field=DateTimeField(),
            )
        )
        .filter(
            start_time__lte=screening_end,
            end_time__gte=screening_start
        )
    )