from django.core.management import BaseCommand
from django.core.management import call_command


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
    )

    def handle(self, *args, **options):
        for name in self.FIXTURES:
            call_command("loaddata", f"{name}.json")
