from collections import defaultdict
import math
from django.core.management.base import BaseCommand

from digital_agenda.apps.estat.models import (
    Dataset,
    Dimension,
    DimensionValue,
    Fact,
)
from digital_agenda.apps.estat.bulk import BulkTSVDataset

from rich.progress import Progress
from rich.console import Console

console = Console()


class Command(BaseCommand):
    help = "Import an Eurostat bulk dataset's data"

    def add_arguments(self, parser):
        parser.add_argument("dataset", type=str.lower, help="Dataset code")
        parser.add_argument(
            "--list-skip-reasons",
            action="store_true",
            default=False,
            help="List skip reasons, per dimension",
        )

    def handle(
        self,
        dataset,
        list_skip_reasons,
        *args,
        **options,
    ):

        bulk_ds = BulkTSVDataset(name=dataset)

        try:
            ds = Dataset.objects.get(code=dataset)
        except Dataset.DoesNotExist:
            console.print(
                f"[red]Dataset {dataset} not found (metadata not imported?).",
            )
            return

        # Must have dataset config
        if ds.config is None:
            console.print(
                f"[red]Dataset {dataset} configuration not found - use the admin site to specify one.",
            )
            return

        # Check single-valued & surrogate dimensions
        for dim in ds.dimensions.all():
            if (
                dim.values.count() > 0
                and dim.single_filtered_value is None
                and not ds.config.has_dimension(dim)
            ):
                console.print(
                    f"[red]Dimension [bold]{dim.code}[not bold] does not have a [bold]single filtered value[not bold] "
                    f"and is missing from dataset [bold]{dataset}[not bold] configuration."
                )
                return

        normalized_dimensions = ("indicator", "breakdown", "unit", "country", "period")

        # Prepare surrogate values, where available
        surrogates = {}
        for dim in normalized_dimensions:
            if (
                getattr(ds.config, dim)
                and getattr(ds.config, dim).code == Dimension.SURROGATE_CODE
            ):
                surrogates[dim] = getattr(ds.config, f"{dim}_surrogate")

        # Caches for dimensions and dimension value instances
        dimensions = {dim.code: dim for dim in ds.dimensions.all()}
        dim_val_cache = {dim.code: {} for dim in ds.dimensions.all()}
        dim_val_disabled_cache = {dim.code: set() for dim in ds.dimensions.all()}
        dim_positions = {
            dim_code: bulk_ds.dimension_codes.index(dim_code)
            for dim_code in bulk_ds.dimension_codes
        }

        Fact.objects.filter(dataset=ds).delete()

        batch_size = 100
        batches = math.ceil(len(bulk_ds.data) / batch_size)
        imported_count = 0
        skip_reasons = defaultdict(set)
        with Progress() as progress:
            batch_task = progress.add_task(
                f"[green]Importing dataset {dataset} bulk facts", total=batches
            )
            for i in range(0, len(bulk_ds.data), batch_size):
                facts_batch = bulk_ds.data[i : i + batch_size]
                fact_objects = []
                for fact in facts_batch:
                    skip_fact = False
                    for idx, dim_code in enumerate(bulk_ds.dimension_codes):
                        fact_val = fact[idx].strip()
                        # Skip rows that don't match single-filtered dimensions
                        if (
                            dimensions[dim_code].single_filtered_value is not None
                            and dimensions[dim_code].single_filtered_value.code
                            != fact_val
                        ):
                            skip_fact = True
                            skip_reasons[dim_code].add(fact_val)
                            break

                        if fact_val in dim_val_disabled_cache[dim_code]:
                            skip_fact = True
                            break
                        else:
                            if fact_val not in dim_val_cache[dim_code]:
                                try:
                                    dim_val_instance = DimensionValue.objects.get(
                                        dimension=dimensions[dim_code], code=fact_val
                                    )
                                    if dim_val_instance.enabled:
                                        dim_val_cache[dim_code][
                                            fact_val
                                        ] = dim_val_instance
                                    else:
                                        skip_fact = True
                                        dim_val_disabled_cache[dim_code].add(fact_val)
                                        skip_reasons[dim_code].add(fact_val)
                                        break
                                except DimensionValue.DoesNotExist:
                                    console.print(
                                        f"[red]Dimension value not found for {dataset} / {dim_code} / {fact_val}",
                                    )
                                    skip_fact = True
                                    break

                    if not skip_fact:
                        fact_dims = {}
                        for norm_dim in normalized_dimensions:
                            if norm_dim in surrogates:
                                fact_dims[norm_dim] = surrogates[norm_dim]
                            else:
                                dim = getattr(ds.config, norm_dim)
                                fact_dims[norm_dim] = dim_val_cache[dim.code][
                                    fact[dim_positions[dim.code]]
                                ]

                        fact_objects.append(
                            Fact(
                                dataset=ds, value=fact[-2], flags=fact[-1], **fact_dims
                            )
                        )

                if fact_objects:
                    Fact.objects.bulk_create(fact_objects)
                    imported_count += len(fact_objects)

                progress.update(batch_task, advance=1)

        console.print(
            f"Imported facts: {imported_count} / {len(bulk_ds.data)}",
        )
        if skip_reasons and list_skip_reasons:
            for dim, values in skip_reasons.items():
                console.print(
                    f"[yellow]Skipped facts with dimension [bold]{dim}[not bold] values: {values}",
                )
