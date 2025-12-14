import factory

from core.factories import LanguageFactory
from movies.models import Director, Genre, Movie


class DirectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Director

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker("word")

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie
        skip_postgeneration_save=True

    title = factory.Faker("sentence", nb_words=3)
    summary = factory.Faker("paragraph")
    release_year = 2025
    poster_image = factory.django.ImageField(color='blue')
    age_restriction = factory.Faker("random_int", min=0, max=21)
    original_language = factory.SubFactory(LanguageFactory)
    director = factory.SubFactory(DirectorFactory)
    duration = 120

    @factory.post_generation
    def genres(self, create: bool, extracted: list[Genre] | None, **kwargs) -> None:
        if not create or not extracted:
            return
        self.genres.add(*extracted)