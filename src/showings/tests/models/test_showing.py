from datetime import timedelta
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from showings.factories import ShowingFactory
from showings.models import Showing

pytestmark = pytest.mark.django_db


def test_showing_string_representation(showing: Showing) -> None:
    showing.start_time = timezone.make_aware(timezone.datetime(2025, 1, 1, 18, 30, 0))
    showing.save(update_fields=["start_time"])

    expected = f"{showing.variant.movie.title} - {showing.start_time} in {showing.theater_hall.number}"
    assert str(showing) == expected


def test_showing_ticket_price_min_value_validation(showing: Showing) -> None:
    showing.ticket_price = Decimal("-0.01")

    with pytest.raises(ValidationError) as exc:
        showing.full_clean()

    assert "ticket_price" in exc.value.message_dict


def test_creating_overlapping_screenings_raises_validation_error(showing: Showing) -> None:
    movie = showing.variant.movie
    movie.duration = 120
    movie.save(update_fields=["duration"])

    start_1 = timezone.now().replace(second=0, microsecond=0) + timedelta(days=1)
    showing.start_time = start_1
    showing.save(update_fields=["start_time"])

    start_2 = start_1 + timedelta(minutes=30)

    overlapping = ShowingFactory.build(
        theater_hall=showing.theater_hall,
        variant=showing.variant,
        start_time=start_2,
        ticket_price=showing.ticket_price,
    )

    with pytest.raises(ValidationError) as exc:
        overlapping.full_clean()

    assert "start_time" in exc.value.message_dict
    assert "overlaps" in exc.value.message_dict["start_time"][0].lower()
