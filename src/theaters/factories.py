import factory
from django.db.models import signals

from theaters.models import Seat, TheaterHall


@factory.django.mute_signals(signals.post_save)
class TheaterHallFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TheaterHall

    number = factory.Sequence(lambda n: f"Hall {n + 1}")

class SeatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seat

    theater_hall = factory.SubFactory(TheaterHallFactory)
    row = factory.Sequence(lambda n: n + 1)
    number = factory.Sequence(lambda n: n + 1)