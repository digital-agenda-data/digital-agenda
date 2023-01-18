import logging
import os

from django.core.cache import caches

logger = logging.getLogger(__name__)


def clear_all_caches(force=False):
    if (
        force or
        # Check if server is running in prod or dev mode
        os.getenv("SERVER_GATEWAY", "").lower() in ("wsgi", "asgi")
        or os.getenv("RUN_MAIN", "").lower() == "true"
    ):
        for key in caches.settings:
            logger.info("Clearing cache %r", key)
            caches[key].clear()
