from django.db.models.signals import post_delete
from django.dispatch import receiver
from movies.models import Movie

@receiver(post_delete, sender=Movie)
def delete_movie_files(sender: type[Movie], instance: Movie, **kwargs) -> None:
    if instance.poster_image:
        instance.poster_image.delete(save=False)