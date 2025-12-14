from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, help_text='The email address of the user.')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(auto_now_add=True, help_text='The date and time when the user joined.')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'User {self.email}'