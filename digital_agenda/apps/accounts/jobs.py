import logging

from django.core.management import call_command

from digital_agenda.common.scheduler import cron

logger = logging.getLogger(__name__)


@cron("0 1 * * *")
def clear_sessions():
    logger.info("Clearing sessions")
    call_command("clearsessions")


@cron("10 1 * * *")
def clear_cas_sessions():
    logger.info("Clearing CAS sessions")
    call_command("django_cas_ng_clean_sessions")


@cron("20 1 * * *")
def disable_inactive_accounts():
    logger.info("Disabling inactive accounts")
    call_command("disable_inactive_accounts")
