from django.apps import AppConfig


class LagnaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lagna'

    def ready(self):
        import apps.lagna.signals