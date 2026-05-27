from django.conf import settings
from django.core.management import BaseCommand, call_command
from rich.console import Console

from digital_agenda.apps.charts.models import (
    BreakdownChartOption,
    Chart,
    ChartFilterOrder,
    ChartFontStyle,
    ChartGroup,
    ExtraChartNote,
    IndicatorChartOption,
)
from digital_agenda.apps.core.models import (
    Breakdown,
    BreakdownGroup,
    BreakdownGroupLink,
    Country,
    CountryProfileIndicator,
    DataSource,
    Indicator,
    IndicatorDataSourceLink,
    IndicatorGroup,
    IndicatorGroupLink,
    Period,
    StaticPage,
    Unit,
)
from digital_agenda.apps.estat.models import GeoGroup, ImportConfig, ImportConfigTag

console = Console()


class Command(BaseCommand):
    help = "Load initial data"

    FIXTURES = (
        # Order is important
        DataSource,
        IndicatorGroup,
        Indicator,
        IndicatorGroupLink,
        BreakdownGroup,
        Breakdown,
        BreakdownGroupLink,
        IndicatorDataSourceLink,
        Unit,
        Period,
        Country,
        CountryProfileIndicator,
        StaticPage,
        # Imports
        GeoGroup,
        ImportConfigTag,
        ImportConfig,
        # Charts
        ChartGroup,
        Chart,
        BreakdownChartOption,
        IndicatorChartOption,
        ExtraChartNote,
        ChartFilterOrder,
        ChartFontStyle,
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-e",
            "--exclude",
            action="append",
            default=[],
            help="Exclude fixtures from the list",
        )
        parser.add_argument(
            "--dump",
            action="store_true",
            default=False,
            help="Dump the data back to the fixtures instead of loading it in the DB",
        )

    def handle(self, *args, exclude, dump=False, **options):
        for model in self.FIXTURES:
            opt = model._meta
            name = opt.model_name
            path = settings.INITIAL_FIXTURES_DIR / f"{name}.json"

            if name in exclude:
                continue

            if dump:
                console.print(f"Dumping fixtures: {path}")
                call_command(
                    "dumpdata",
                    "--indent",
                    "4",
                    "-o",
                    str(path),
                    "--natural-foreign",
                    "--natural-primary",
                    f"{opt.app_label}.{name}",
                )
            else:
                console.print(f"Loading from fixture: '{name}'")
                call_command("loaddata", name)
