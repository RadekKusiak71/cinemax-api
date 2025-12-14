from django.apps import AppConfig


class TheatersConfig(AppConfig):
    name = 'theaters'

    def ready(self) -> None:
        import theaters.signals