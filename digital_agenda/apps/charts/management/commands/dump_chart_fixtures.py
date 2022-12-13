from django.conf import settings
from django.core.management import BaseCommand
from django.core.management import call_command
from rich.console import Console

console = Console()


class Command(BaseCommand):
    def dump_fixture(self, model, filename, **options):
        console.print(f"Dumping '{model}' to fixtures")

        fixtures_dir = (
            settings.BASE_DIR / "digital_agenda" / "apps" / "charts" / "fixtures"
        )

        call_command(
            "dumpdata",
            "--indent",
            "2",
            "-o",
            str(fixtures_dir / (filename + ".json")),
            model,
            **options,
        )

    def handle(self, *args, **options):
        self.dump_fixture("charts.ChartGroup", "chartgroups", **options)
        self.dump_fixture("charts.Chart", "charts", **options)
