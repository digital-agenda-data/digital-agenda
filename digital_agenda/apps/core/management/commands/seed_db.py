import itertools
import sys

from django.conf import settings
from django.core.files import File
from django.core.management import BaseCommand
from django.core.management import call_command
from rich.console import Console

from digital_agenda.apps.charts.models import BreakdownChartOption
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.models import IndicatorChartOption
from digital_agenda.apps.core.cache import clear_all_caches

console = Console()
TEST_FIXTURES = [
    # Create users / password:
    #  - admin@example.com / admin
    #  - user@example.com / user
    #  - inactive@example.com / inactive:
    "test/users",
    # Import some testing extra notes
    "test/extra-chart-notes",
    # Import some breakdown chart options for testing
    "test/breakdown-chart-options",
    # Import some facts
    "test/facts",
    # Import some data for DESI (with extra notes indicators)
    "test/desi-extra-notes-facts",
    # Import some data for Digital Decade indicators and trajectories
    "test/digital-trajectory-facts",
    # Import some data for Digital Economy and Society Index (until 2022)
    "test/desi-facts",
    # Import some data for Country Profile
    "test/country-profile-facts",
    # Import some test charts with custom options
    "test/chartgroup",
    "test/chart",
    "test/chartfilterorder",
    "test/chartfontstyle",
    # Import some facts from some small ESTAT configs
    "test/seed_importconfigs",
]


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

        for name in TEST_FIXTURES:
            console.print(f"Loading from fixture: '{name}'")
            call_command("loaddata", name)

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
