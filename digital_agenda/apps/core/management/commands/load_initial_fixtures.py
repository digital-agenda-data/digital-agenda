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

    def handle(self, *args, **options):
        for name in self.FIXTURES:
            console.print(f"Loading from fixture: '{name}'")
            call_command("loaddata", f"{name}.json")
