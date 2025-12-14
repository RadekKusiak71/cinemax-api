from django.db.models.signals import post_save
from django.dispatch import receiver

from theaters.models import Seat, TheaterHall


@receiver(post_save, sender=TheaterHall)
def theater_hall_post_save_seats_generate(sender: type[TheaterHall], instance: TheaterHall, created: bool, **kwargs) -> None:
    if not created:
        return
    
    seats_to_create: list[Seat] = []

    for row in range(1, 8):
        for number in range(1, 12):
            seats_to_create.append(
                Seat(
                    theater_hall=instance, 
                    row=row, 
                    number=number
                )
            )

    Seat.objects.bulk_create(seats_to_create)

    
    
