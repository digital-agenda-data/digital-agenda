import logging

from django.core.exceptions import ValidationError

from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.estat.importer import EstatImporter
from digital_agenda.apps.estat.importer import ImporterError
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
        except ValidationError as exc:
            task.errors = exc.message_dict
            raise
        except ImporterError as exc:
            task.errors = exc.args[0]
            raise
        except Exception as exc:
            task.errors = {
                "Unexpected error": str(exc),
            }
            raise
        finally:
            task.save()
            clear_all_caches(force=True)
