import os

from django.apps import AppConfig

from digital_agenda.apps.core.cache import clear_all_caches


class Config(AppConfig):
    name = "digital_agenda.apps.core"
    verbose_name = "Core"
    auto_clear_cache = True

    def ready(self):
        import digital_agenda.apps.core.signals  # noqa

        if os.getenv("SERVER_GATEWAY", "").lower() in ("wsgi", "asgi"):
            # Auto clear caches when app starts
            clear_all_caches()

        if os.getenv("RUN_MAIN", "").lower() == "true":
            # Running in "runserver" mode, also clear cache
            clear_all_caches()
