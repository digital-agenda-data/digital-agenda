import logging

import constance
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.mail import send_mail
from django_rq import job

from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.estat.importer import DryRunEstatImporter
from digital_agenda.apps.estat.importer import EstatDataflow
from digital_agenda.apps.estat.importer import EstatImporter
from digital_agenda.apps.estat.importer import ImporterError
from digital_agenda.apps.estat.models import ImportConfig
from digital_agenda.common.job import LoggingJob
from digital_agenda.common.scheduler import cron
from digital_agenda.common.utils import reverse_absolute_uri
from digital_agenda.common.utils import split_email

logger = logging.getLogger(__name__)
User = get_user_model()


class ImportFromConfigJob(LoggingJob):
    @classmethod
    def _execute_import(cls, task):
        config = task.import_config
        importer = EstatImporter(config, force_download=task.force_download)
        logger.info("Processing config %r: %r", config, config.title)
        logger.info("Config %r filters=%r", config, config.filters)
        logger.info("Config %r mappings=%r", config, config.mappings)
        logger.info("Config %r multipliers=%r", config, config.multipliers)

        if task.delete_existing:
            result = Fact.objects.filter(import_config=importer.config).delete()
            logger.info("Deleted Facts: %s", result)

        importer.run()

    @classmethod
    def _execute_dry_run(cls, task):
        importer = DryRunEstatImporter(
            task.import_config, force_download=task.force_download
        )
        logger.info("Processing config: %r", importer.config)
        importer.run()
        task.dry_run_report = File(importer.get_xlsx())

    @classmethod
    def execute_with_logging(cls, job, task):
        try:
            if task.dry_run:
                cls._execute_dry_run(task)
            else:
                cls._execute_import(task)
        except ValidationError as exc:
            task.errors = exc.message_dict
            raise
        except ImporterError as exc:
            task.errors = exc.args[0]
            raise
        except Exception as exc:
            task.errors = {"Unexpected error": str(exc)}
            raise
        finally:
            task.save()
            clear_all_caches(force=True)


UPDATE_ALERT_SUBJECT = "[Digital Agenda Data] %(config_count)s import configurations with new version available"
UPDATE_ALERT_TEMPLATE = """Hello,

%(config_count)s import configurations currently have new version available in ESTAT 
and require reimporting.

Full list can be viewed by clicking on this link:

    %(list_url)s

"""


@cron("0 10 * * MON")
def send_estat_update_alerts():
    config_count = ImportConfig.objects.filter(
        new_version_available=True,
        disable_check_updates=False,
    ).count()
    if not config_count:
        logger.info("No import config has a new version available")
        return

    recipient_list = split_email(constance.config.ESTAT_UPDATE_ALERT_EMAILS or "")
    if not recipient_list:
        recipient_list = User.objects.filter(is_staff=True).values_list(
            "email", flat=True
        )

    if not recipient_list:
        raise Exception("No recipients configured to receive alerts")

    context = {
        "config_count": config_count,
        "list_url": (
            reverse_absolute_uri("admin:estat_importconfig_changelist")
            + "?new_version_available__exact=1"
        ),
    }
    send_mail(
        UPDATE_ALERT_SUBJECT % context,
        UPDATE_ALERT_TEMPLATE % context,
        None,
        recipient_list,
    )


@cron("0 0 * * *")
def check_all_configs_for_updates():
    # Don't check configs that already have the "new version available" flag already set.
    for estat_code in (
        ImportConfig.objects.filter(
            datastructure_last_version__isnull=False,
            new_version_available=False,
            disable_check_updates=False,
        )
        .values_list("code", flat=True)
        .distinct("code")
    ):
        # Set ID to avoid queuing a duplicate task if one is in the queue already.
        check_estat_dataset_for_updates.delay(
            estat_code, job_id=f"check_estat_dataset_for_updates({estat_code})"
        )


@job
def check_estat_dataset_for_updates(code):
    logger.info("Checking %s for updates", code)

    dataflow = EstatDataflow(code)
    for config in ImportConfig.objects.filter(
        code=code, new_version_available=False, disable_check_updates=False
    ):
        if (
            # andrei, disable checking the dsd version
            # dataflow.version != config.datastructure_last_version or
            dataflow.update_data != config.data_last_update
            or dataflow.update_structure != config.datastructure_last_update
        ):
            logger.info("New version available for config %s: %s", config, dataflow)
            config.new_version_available = True
            config.save()
