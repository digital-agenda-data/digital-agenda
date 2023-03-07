import logging

from digital_agenda.common.job import LoggingJob
from .cache import clear_all_caches
from .formats import get_loader
from .models import Fact

logger = logging.getLogger(__name__)


class ImportFromDataFileJob(LoggingJob):
    @staticmethod
    def execute_with_logging(job, task):
        data_file = task.import_file

        loader = get_loader(data_file, extra_fields={"import_file": data_file})
        errors = None

        try:
            if task.delete_existing:
                result = Fact.objects.filter(import_file=data_file).delete()
                logger.info("Deleted Facts: %s", result)

            facts_count, errors = loader.load(allow_errors=False)
            logger.info(
                "Loaded %s facts from data file %s", facts_count, data_file.path
            )
            if errors:
                raise ValueError()
        except Exception as exc:
            if errors:
                task.errors = errors
                task.save()
                logger.error(
                    "Could not import data file %s: %s", data_file.path.name, errors
                )
            else:
                logger.error(
                    "Could not import data file %s: %s", data_file.path.name, exc
                )
            raise
        finally:
            clear_all_caches(force=True)
