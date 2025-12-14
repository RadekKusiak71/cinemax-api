import factory

from reservations.models import Reservation, Ticket


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    user = factory.SubFactory('users.factories.UserFactory')
    showing = factory.SubFactory('showings.factories.ShowingFactory')
    full_price = 20.00

class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    reservation = factory.SubFactory(ReservationFactory)
    seat = factory.SubFactory(
        'theaters.factories.SeatFactory', 
        theater_hall=factory.SelfAttribute('..reservation.showing.theater_hall')
    )
    price = 10.00