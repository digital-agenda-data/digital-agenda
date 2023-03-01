from celery import shared_task, states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from django.apps import apps

from .formats import get_loader

logger = get_task_logger(__name__)


@shared_task(bind=True)
def import_data_file(self, data_file_pk):
    DataFileImport = apps.get_model("core.DataFileImport")  # noqa
    try:
        data_file = DataFileImport.objects.get(id=data_file_pk)
    except DataFileImport.DoesNotExist:
        self.update_state(state=states.FAILURE)
        logger.error("Data file not found for pk %s", data_file_pk)
        raise Ignore()

    loader = get_loader(data_file, extra_fields={"import_file": data_file})
    errors = None

    data_file.status = DataFileImport.ImportStatusChoices.IN_PROGRESS
    data_file.save()

    try:
        facts_count, errors = loader.load(allow_errors=False)
        logger.info("Loaded %s facts from data file %s", facts_count, data_file.path)
        if errors:
            raise ValueError()
        data_file.status = DataFileImport.ImportStatusChoices.SUCCESS
        data_file.save()
    except Exception as exc:
        if errors:
            data_file.errors = errors
            logger.error(
                "Could not import data file %s: %s", data_file.path.name, errors
            )
        else:
            logger.error("Could not import data file %s: %s", data_file.path.name, exc)

        data_file.status = DataFileImport.ImportStatusChoices.FAILED
        data_file.save()

        self.update_state(state=states.FAILURE, meta=exc)
        raise Ignore()
