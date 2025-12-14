import factory

from core.models import Language


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language
        django_get_or_create = ('code', 'name',)

    name = factory.Faker('language_name')
    code = factory.Faker('language_code')