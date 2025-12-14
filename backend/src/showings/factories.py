from datetime import timedelta
from decimal import Decimal

import factory
from django.utils import timezone

from showings.models import Showing, ShowingFormat, ShowingVariant


class ShowingFormatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShowingFormat
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Format {n}')

class ShowingVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShowingVariant
        django_get_or_create = ('movie', 'format', 'subtitles', 'dubbing')

    movie = factory.SubFactory('movies.factories.MovieFactory')
    format = factory.SubFactory(ShowingFormatFactory)
    subtitles = None
    dubbing = None

class ShowingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Showing

    theater_hall = factory.SubFactory('theaters.factories.TheaterHallFactory')
    variant = factory.SubFactory(ShowingVariantFactory)
    start_time = factory.Sequence(lambda n: timezone.now() + timedelta(days=n))
    ticket_price = Decimal('10.00')