from django.apps import AppConfig


class MedicalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "medical"

    def ready(self):
        # from . import signals
        return super().ready()
