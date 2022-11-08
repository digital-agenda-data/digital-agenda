import argparse
import orjson

from django.core.management.base import BaseCommand
from django.db.models import Case, When
from rich.console import Console

from digital_agenda.apps.estat.models import (
    Dataset,
    Dimension,
    DimensionValue,
)


console = Console()


class Command(BaseCommand):
    help = (
        "Enable dimensions values of Eurostat datasets based on input file."
        " All other values are disabled."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=argparse.FileType("rb"), help="Dataset code"
        )

    def handle(self, json_file, *args, **options):
        input_data = orjson.loads(json_file.read())
        for dataset_code, dataset_config in input_data.items():
            try:
                dataset = Dataset.objects.get(code=dataset_code)
                console.print(f"Dataset [bold]'{dataset_code}'[/]")
                for dimension_code, values in dataset_config.items():
                    console.print(f"\t- dimension [bold]'{dimension_code}'[/]")
                    values_to_enable = set(values)
                    try:
                        dimension = Dimension.objects.get(
                            dataset=dataset, code=dimension_code
                        )
                        matching_values = set(
                            v.lower()
                            for v in list(
                                DimensionValue.objects.filter(
                                    dimension=dimension, code__in=values_to_enable
                                ).values_list("code", flat=True)
                            )
                        )
                        if matching_values < values_to_enable:
                            console.print(
                                f"\t\t[yellow]values not found (will be ignored): "
                                f"{list(values_to_enable - matching_values)}"
                            )
                        DimensionValue.objects.filter(dimension=dimension).update(
                            enabled=Case(
                                When(code__in=values_to_enable, then=True),
                                default=False,
                            )
                        )
                        console.print(
                            f"\t\t[green]values enabled: {list(matching_values)}."
                        )
                    except Dimension.DoesNotExist:
                        console.print(
                            f"\t[red]dimension [bold]'{dimension_code}'[/] not found!"
                        )

            except Dataset.DoesNotExist:
                console.print(f"[red]Dataset [bold]'{dataset_code}'[/] not found!")
