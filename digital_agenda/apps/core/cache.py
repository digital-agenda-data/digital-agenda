import logging

from django.core.cache import caches

logger = logging.getLogger(__name__)


def clear_all_caches():
    for key in caches.settings:
        logger.info("Clearing cache %r", key)
        caches[key].clear()
