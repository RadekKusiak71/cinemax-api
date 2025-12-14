from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q


class Command(BaseCommand):

    def handle_credentials(self) -> tuple[str, str]:
        email = config('DJANGO_ADMIN_EMAIL')
        password = config('DJANGO_ADMIN_PASSWORD')

        if not email:
            raise CommandError('DJANGO_ADMIN_EMAIL is not set in environment variables.')
        
        if not password:
            raise CommandError('DJANGO_ADMIN_PASSWORD is not set in environment variables.')

        return email, password

    def handle(self, *args, **options) -> None:
        User = get_user_model()
        email, password = self.handle_credentials()

        if User.objects.filter(
            Q(email=email) |
            Q(is_superuser=True)
        ).exists():
            self.stdout.write(self.style.WARNING('An admin account already exists.'))
        else:
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin account with email {email}.'))
