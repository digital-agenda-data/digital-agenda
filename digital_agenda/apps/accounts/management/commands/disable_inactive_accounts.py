"""Expire accounts that have not logged in a certain amount of time."""
import logging
from datetime import timedelta

from constance import config
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--days",
            type=int,
            default=config.USER_INACTIVE_DAYS,
            help="Number of days of inactivity required for the account to expire",
        )

    def handle(self, *args, days, **options):
        assert days >= 0, "Number of days must be a positive integer"
        if not days:
            logger.info("Inactive account expiry is disabled.")
            return

        limit = timezone.now() - timedelta(days=days)
        logger.info(
            "Disabling accounts that have not logged in since %s days ago: %s",
            days,
            limit,
        )
        for user in User.objects.filter(is_active=True):
            # If the user never logged in, check the created date instead
            reference_date = user.last_login or user.created_at
            logger.debug("User %s last login on %s", user, reference_date)
            if reference_date >= limit:
                continue

            logger.info(
                "User %s has not logged in since %s, setting account to inactive",
                user,
                reference_date,
            )
            user.is_active = False
            user.save()
