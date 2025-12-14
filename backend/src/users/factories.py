import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)
    
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.django.Password('!QAZ2wsx!@#!@#')