import logging

from celery import shared_task
from django.utils import timezone

from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.estat.estat_import import EstatImporter

logger = logging.getLogger(__name__)


@shared_task
def import_from_config(config_pk, force_download=False, delete_existing=False):
    importer = EstatImporter(config_pk, force_download=force_download)
    logger.info("Processing config: %r", importer.config)
    importer.config.status = "Running"
    importer.config.save()
    importer.config.refresh_from_db()

    try:
        if delete_existing:
            result = Fact.objects.filter(import_config=importer.config).delete()
            logger.info("Deleted Facts: %s", result)

        importer.run()
        importer.config.status = "Completed"
    except Exception as e:
        logger.exception("Unable to finish import: %s", e)
        importer.config.status = str(e) or "Unknown Error"
    finally:
        importer.config.last_import_time = timezone.now()
        importer.config.save()
        clear_all_caches(force=True)
