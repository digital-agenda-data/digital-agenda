import logging
import os

from django.apps import AppConfig
from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.common.scheduler import clear_scheduler

logger = logging.getLogger(__name__)


class Config(AppConfig):
    name = "digital_agenda.apps.core"
    verbose_name = "Core"
    auto_clear_cache = True

    def ready(self):
        # Auto clear caches when app starts
        clear_all_caches()

        if os.environ.get(DJANGO_AUTORELOAD_ENV) == "true":
            # If we are auto-reloading code, make sure to remove any cron/scheduled
            # jobs as that may have changed as well
            clear_scheduler()

        import digital_agenda.apps.core.jobs  # noqa
        import digital_agenda.apps.core.signals  # noqa
