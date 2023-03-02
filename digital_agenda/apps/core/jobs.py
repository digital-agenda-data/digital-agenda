import logging

from django_rq import job

from .formats import get_loader
from .models import DataFileImport
from .models import Fact

logger = logging.getLogger(__name__)


@job
def import_data_file(data_file_pk, delete_existing=False):
    try:
        data_file = DataFileImport.objects.get(id=data_file_pk)
    except DataFileImport.DoesNotExist:
        logger.error("Data file not found for pk %s", data_file_pk)
        raise

    loader = get_loader(data_file, extra_fields={"import_file": data_file})
    errors = None

    data_file.status = DataFileImport.ImportStatusChoices.IN_PROGRESS
    data_file.save()

    try:
        if delete_existing:
            result = Fact.objects.filter(import_file=data_file).delete()
            logger.info("Deleted Facts: %s", result)

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
        raise
