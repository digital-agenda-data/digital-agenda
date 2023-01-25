import sys

from django.core.management import BaseCommand
from django.core.management import call_command

from digital_agenda.apps.core.models import Fact


class Command(BaseCommand):
    help = "Seed DB for E2E tests"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            help="Do not prompt for any user input",
            default=False,
        )

    def handle(self, *args, noinput=False, **options):
        if not noinput:
            print(
                "This will IRREVERSIBLY DESTROY all data currently in the  database! "
                "Are you sure you want to continue?",
                end=" ",
            )
            if input("[Y/n] ") != "Y":
                sys.exit(1)

        call_command("flush", "--noinput")
        call_command("load_initial_fixtures", "--test")

        for fact in Fact.objects.all():
            fact.indicator.units.add(fact.unit)
            fact.indicator.periods.add(fact.period)
            fact.indicator.countries.add(fact.country)
            fact.indicator.breakdowns.add(fact.breakdown)
            fact.indicator.save()