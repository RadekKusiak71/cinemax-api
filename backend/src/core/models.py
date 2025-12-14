from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="ISO 639-1 language code (e.g., 'EN' for English)")

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'
