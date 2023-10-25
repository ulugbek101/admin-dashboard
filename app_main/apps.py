from django.apps import AppConfig


class AppMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_main'

    def ready(self):
        from . import signals