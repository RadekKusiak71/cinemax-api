import typing

from django.contrib.auth.base_user import BaseUserManager

if typing.TYPE_CHECKING:
    from users.models import User


class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str = None, **extra_fields) -> 'User':
        if not email:
            raise ValueError('The Email field must be set')
        email: str = self.normalize_email(email)
        user: 'User' = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str = None, **extra_fields) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)