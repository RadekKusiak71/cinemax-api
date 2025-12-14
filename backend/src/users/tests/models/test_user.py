import faker
import pytest
from django.core.exceptions import ValidationError

from users.factories import UserFactory
from users.models import User

pytestmark = pytest.mark.django_db

def test_user_str_repr(user: User) -> None:
    assert str(user) == f"User {user.email}"

def test_user_email_uniqueness(user: User, user_factory: UserFactory) -> None:
    with pytest.raises(ValidationError) as exc_info:
        new_user: User = user_factory.build(email=user.email)
        new_user.full_clean()

    assert 'email' in exc_info.value.message_dict
    assert exc_info.value.message_dict['email'] == ['User with this Email already exists.']

def test_user_default_fields(user: User) -> None:
    assert user.is_active is True
    assert user.is_staff is False
    assert user.date_joined is not None

@pytest.mark.parametrize('email', ['', None])
def test_create_user_without_email_raises_error(email: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        User.objects.create_user(email=email)

    assert str(exc_info.value) == 'The Email field must be set'

def test_create_superuser_with_is_staff_false_raises_error(faker: faker.Faker) -> None:
    with pytest.raises(ValueError) as exc_info:
        User.objects.create_superuser(email=faker.email(), is_staff=False)
    assert str(exc_info.value) == 'Superuser must have is_staff=True.'

def test_create_superuser_with_is_superuser_false_raises_error(faker: faker.Faker) -> None:
    with pytest.raises(ValueError) as exc_info:
        User.objects.create_superuser(email=faker.email(), is_superuser=False)
    assert str(exc_info.value) == 'Superuser must have is_superuser=True.'