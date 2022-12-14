from django.apps import AppConfig

from digital_agenda.apps.core.cache import clear_all_caches


class Config(AppConfig):
    name = "digital_agenda.apps.core"
    verbose_name = "Core"
    auto_clear_cache = True

    def ready(self):
        import digital_agenda.apps.core.signals  # noqa

        # Auto clear caches when app starts
        clear_all_caches()
