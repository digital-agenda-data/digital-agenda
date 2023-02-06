from django.core.management import BaseCommand
from django.core.management import call_command
from rich.console import Console

console = Console()


class Command(BaseCommand):
    help = "Load initial data"

    FIXTURES = (
        # Order is important
        "datasources",
        "indicatorgroups",
        "indicators",
        "indicatorgrouplinks",
        "breakdowngroups",
        "breakdowns",
        "breakdowngrouplinks",
        "datasourcelinks",
        "units",
        "periods",
        "countries",
        # Imports
        "geogroups",
        "importconfigs",
        # Charts
        "chartgroups",
        "charts",
    )
    TEST_FIXTURES = (
        "test/facts",
        "test/users",
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--test", action="store_true", help="Also load test fixtures"
        )
        parser.add_argument(
            "-e",
            "--exclude",
            action="append",
            default=[],
            help="Exclude fixtures from the list",
        )

    def handle(self, *args, exclude, test=False, **options):
        fixtures = self.FIXTURES
        if test:
            fixtures += self.TEST_FIXTURES

        for name in fixtures:
            if name in exclude:
                continue
            console.print(f"Loading from fixture: '{name}'")
            call_command("loaddata", f"{name}.json")
