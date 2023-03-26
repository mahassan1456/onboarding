from django.apps import AppConfig


class PproductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pproducts"

    def ready(self):
        from . import signals
        return super().ready()
