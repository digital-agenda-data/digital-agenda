from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "digital_agenda.apps.estat"
    verbose_name = "Eurostat"

    def ready(self):
        import digital_agenda.apps.estat.jobs  # noqa
