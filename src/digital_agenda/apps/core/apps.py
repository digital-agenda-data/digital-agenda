from django.apps import AppConfig


class Config(AppConfig):
    name = "digital_agenda.apps.core"
    verbose_name = "Core"

    def ready(self):
        import digital_agenda.apps.core.signals  # noqa
