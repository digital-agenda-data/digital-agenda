from django.apps import AppConfig


class Config(AppConfig):
    name = "digital_agenda.apps.core"
    verbose_name = "Core"
    auto_clear_cache = True

    def ready(self):
        import digital_agenda.apps.core.signals  # noqa
