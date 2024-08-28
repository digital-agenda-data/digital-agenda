from django.core.management import BaseCommand
from rich.console import Console

from digital_agenda.apps.charts.models import ExtraChartNote
from digital_agenda.apps.core.models import Fact

console = Console()


class Command(BaseCommand):
    help = "Migrate extra chart notes model"

    def handle(self, *args, **options):
        for obj in ExtraChartNote.objects.all():
            reference_period = int(obj.note.strip()[-5:-1])
            assert reference_period > 2000

            count = Fact.objects.filter(
                indicator=obj.indicator, period=obj.period
            ).update(reference_period=str(reference_period))
            console.print(f"{obj} migrated to {count} Fact objects")
