import logging

from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.estat.importer import EstatImporter
from digital_agenda.common.job import LoggingJob

logger = logging.getLogger(__name__)


class ImportFromConfigJob(LoggingJob):
    @staticmethod
    def execute_with_logging(job, task):
        try:
            importer = EstatImporter(
                task.import_config, force_download=task.force_download
            )
            logger.info("Processing config: %r", importer.config)

            if task.delete_existing:
                result = Fact.objects.filter(import_config=importer.config).delete()
                logger.info("Deleted Facts: %s", result)

            importer.run()
            clear_all_caches(force=True)
        except Exception as exc:
            if len(exc.args) > 0:
                task.errors = exc.args[0]
                task.save()
            raise
        finally:
            clear_all_caches(force=True)
