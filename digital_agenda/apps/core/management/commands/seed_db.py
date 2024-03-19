import itertools
import sys

from django.conf import settings
from django.core.files import File
from django.core.management import BaseCommand
from django.core.management import call_command

from digital_agenda.apps.charts.models import BreakdownChartOption
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.models import IndicatorChartOption
from digital_agenda.apps.core.cache import clear_all_caches


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
        call_command("load_initial_fixtures", "--exclude", "importconfig")

        # Create users / password:
        #  - admin@example.com / admin
        #  - user@example.com / user
        #  - inactive@example.com / inactive:
        call_command("loaddata", "test/users")

        # Import some testing extra notes
        call_command("loaddata", "test/extra-chart-notes")

        # Import some facts
        call_command("loaddata", "test/facts")

        # Import some data for DESI (with extra notes indicators)
        call_command("loaddata", "test/desi-extra-notes-facts")

        # Import some data for Digital Decade indicators and trajectories
        call_command("loaddata", "test/digital-trajectory-facts")

        # Import some data for Digital Economy and Society Index (until 2022)
        call_command("loaddata", "test/desi-facts")

        # Import some test charts with custom options
        call_command("loaddata", "test/chartgroup")
        call_command("loaddata", "test/chart")
        call_command("loaddata", "test/chartfilterorder")
        call_command("loaddata", "test/chartfontstyle")

        # Import some facts from some small ESTAT configs
        call_command("loaddata", "test/seed_importconfigs")
        call_command("estat_import")

        for group in ChartGroup.objects.all():
            try:
                img_path = settings.TEST_FIXTURES_DIR / f"{group.code}.png"
                with img_path.open("rb") as f:
                    group.image = File(f, name=img_path.name)
                    group.save()
            except OSError:
                continue

        dd_img = settings.TEST_FIXTURES_DIR / "dd_target.webp"
        for opt in itertools.chain(
            BreakdownChartOption.objects.all(),
            IndicatorChartOption.objects.all(),
        ):
            if not opt.custom_symbol:
                continue

            with dd_img.open("rb") as f:
                opt.custom_symbol = File(f, name=dd_img.name)
                opt.save()

        clear_all_caches(force=True)
