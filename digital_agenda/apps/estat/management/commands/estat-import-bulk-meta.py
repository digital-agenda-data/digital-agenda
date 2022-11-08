from django.core.management.base import BaseCommand
from django.db import transaction
from rich.console import Console

from digital_agenda.apps.estat.models import (
    Dataset,
    Dimension,
    DimensionValue,
)
from digital_agenda.apps.estat.bulk import BulkTSVDataset


console = Console()


class Command(BaseCommand):
    help = "Import an Eurostat bulk dataset's metadata."

    def add_arguments(self, parser):
        parser.add_argument("dataset_code", type=str.lower, help="Dataset code")
        parser.add_argument(
            "--delete-existing",
            action="store_true",
            default=False,
            help="Delete existing data",
        )
        parser.add_argument(
            "--indicator", type=str.lower, help="Indicator dimension/surrogate value"
        )
        parser.add_argument(
            "--breakdown", type=str.lower, help="Breakdown dimension/surrogate value"
        )
        parser.add_argument(
            "--unit", type=str.lower, help="Unit dimension/surrogate value"
        )
        parser.add_argument(
            "--country", type=str.lower, help="Country dimension/surrogate value"
        )
        parser.add_argument(
            "--period", type=str.lower, help="Period dimension/surrogate value"
        )

    def handle(
        self,
        dataset_code,
        delete_existing,
        indicator,
        breakdown,
        unit,
        country,
        period,
        *args,
        **options,
    ):

        console.print(
            f"[green]Importing [bold]{dataset_code}",
            new_line_start=True,
        )

        bulk_ds = BulkTSVDataset(name=dataset_code)

        if delete_existing:
            try:
                Dataset.objects.get(code=dataset_code).delete()
                console.print(
                    "[yellow]\t- existing dataset deleted.",
                    new_line_start=True,
                )
            except Dataset.DoesNotExist:
                pass

        console.print(
            "\t- importing dataset & dimensions metadata ... ",
            end="",
            new_line_start=True,
        )

        try:
            with transaction.atomic():
                dataset, _ = Dataset.objects.update_or_create(
                    code=dataset_code, defaults={"label": bulk_ds.label or ""}
                )

                bulk_ds.populate_dimension_values()
                bulk_ds.populate_dimension_labels()

                for dim in list(bulk_ds.dimensions.values()):
                    dimension, _ = Dimension.objects.update_or_create(
                        dataset=dataset,
                        code=dim.code,
                        defaults={"label": dim.label or ""},
                    )
                    for val in dim.values.values():
                        DimensionValue.objects.update_or_create(
                            dimension=dimension,
                            code=val.code,
                            defaults={
                                "label": val.label or "",
                                # Indicator values default to disabled, to avoid accidental imports of unwanted data
                                "enabled": False if dim.code == indicator else True,
                            },
                        )

        except Exception:  # noqa
            console.print("[red]FAILED")
            console.print_exception(show_locals=True)
            exit(1)

        for dim_name in ("indicator", "breakdown", "unit", "country", "period"):
            input_dim = locals()[dim_name]
            if input_dim is None:
                console.print(
                    f"[yellow] Missing config for {dataset_code} {dim_name}"
                    " - make sure to provide one in the admin site.",
                    new_line_start=True,
                )
                continue

            if input_dim.startswith("~"):
                try:
                    dimension = Dimension.objects.get(
                        dataset=dataset, code=Dimension.SURROGATE_CODE
                    )
                    setattr(dataset.config, dim_name, dimension)
                    surrogate, _ = DimensionValue.objects.get_or_create(
                        dimension=dimension, code=input_dim[1:]
                    )
                    setattr(dataset.config, f"{dim_name}_surrogate", surrogate)
                except Dimension.DoesNotExist:
                    console.print(
                        f"[red]Surrogate dimension for {dataset_code} does not exist."
                    )
                    exit(1)
            else:
                try:
                    dimension = Dimension.objects.get(dataset=dataset, code=input_dim)
                    setattr(dataset.config, dim_name, dimension)
                except Dimension.DoesNotExist:
                    console.print(
                        f"[red]Dimension for {dataset_code} not found: {input_dim}"
                    )
                    exit(1)

        dataset.config.save()

        console.print("[green]DONE")
