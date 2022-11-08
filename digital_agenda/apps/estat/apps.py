from django.apps import AppConfig


class Config(AppConfig):
    name = "digital_agenda.apps.estat"
    verbose_name = "Eurostat"

    def ready(self):
        import digital_agenda.apps.estat.signals  # noqa
