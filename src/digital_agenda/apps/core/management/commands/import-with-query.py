import math

from django.core.management.base import BaseCommand
from django.db import connection

from django_sql_dashboard.models import DashboardQuery

from rich.progress import Progress
from rich.console import Console

from digital_agenda.apps.core.models import (
    DataSource,
    Indicator,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)

from digital_agenda.apps.estat.models import Dataset, DimensionValue

console = Console()


class Command(BaseCommand):
    help = "Run an import based on a dashboard-stored query"

    def add_arguments(self, parser):
        parser.add_argument("dashboard_slug", type=str.lower, help="Dashboard slug")
        parser.add_argument("--batch-size", type=int, default=1000, help="Batch size")

    def handle(
        self,
        dashboard_slug,
        batch_size,
        *args,
        **options,
    ):
        query = DashboardQuery.objects.filter(dashboard__slug=dashboard_slug).first()
        if query is None:
            console.print("[red]Dashboard not found or no query defined.")
            exit(1)

        with connection.cursor() as cursor:
            with Progress(transient=True) as progress:
                task = progress.add_task("Executing query", total=None, start=False)
                cursor.execute(query.sql)
                progress.update(task, completed=True)

            query_results = cursor.fetchall()
            console.print(f"Facts in query results: {len(query_results)}")

        console.print("Deleting existing facts ... ", end="")
        indicators = set([r[1] for r in query_results])
        indicator_recs = Indicator.objects.filter(code__in=indicators).all()
        facts_q = Fact.objects.filter(indicator__in=indicator_recs)
        existing_facts_count = facts_q.count()
        if existing_facts_count > 0:
            Fact.objects.filter(indicator__in=indicator_recs).delete()
            console.print(f"DONE ({existing_facts_count} deleted)")
        else:
            console.print("NONE FOUND")

        # Caches of pairs of object instances and "created" flags, indexed by dimension values
        # in the query results
        data_sources = {}
        datasets = {}
        dims = ("indicator", "breakdown", "unit", "country", "period")
        dim_plurals = {
            dim: f"{dim}s" if dim != "country" else "countries" for dim in dims
        }
        dim_models = {
            "indicator": Indicator,
            "breakdown": Breakdown,
            "unit": Unit,
            "country": Country,
            "period": Period,
        }
        dims_cache = {d: {} for d in dims}
        batches = math.ceil(len(query_results) / batch_size)
        imported_count = 0

        with Progress() as progress:
            batch_task = progress.add_task(
                f"[green]Importing facts for dashboard query {dashboard_slug}",
                total=batches,
            )
            for i in range(0, len(query_results), batch_size):
                results_batch = query_results[i : i + batch_size]
                fact_objects = []
                row_dims = {d: None for d in dims}
                for row in results_batch:
                    (
                        estat_dataset,
                        row_dims["indicator"],
                        row_dims["breakdown"],
                        row_dims["unit"],
                        row_dims["country"],
                        row_dims["period"],
                        value,
                        flags,
                    ) = row

                    dataset = f"estat_{estat_dataset}"

                    # Datasets are kept as data source references
                    if dataset not in data_sources:
                        data_sources[dataset] = DataSource.objects.get_or_create(
                            code=dataset
                        )

                    # Indicator records need to be set up before the rest of the dimensions,
                    # which are all M2M-related to indicators.
                    if row_dims["indicator"] not in dims_cache["indicator"]:
                        dims_cache["indicator"][
                            row_dims["indicator"]
                        ] = Indicator.objects.update_or_create(
                            code=row_dims["indicator"],
                            defaults={
                                "data_source": data_sources[dataset][0],
                            },
                        )

                    # The Eurostat dataset will be used to dig for labels.
                    if dataset not in datasets:
                        datasets[dataset] = Dataset.objects.get(code=estat_dataset)

                    # The rest of the dimensions
                    for dim, dim_cache in dims_cache.items():
                        if dim == "indicator":
                            continue

                        if row_dims[dim] not in dim_cache:
                            dim_cache[row_dims[dim]] = dim_models[
                                dim
                            ].objects.get_or_create(code=row_dims[dim])
                            # For new values, attempt to source label from ESTAT dimension values
                            if dim_cache[row_dims[dim]][1]:
                                try:
                                    if getattr(datasets[dataset].config, dim):
                                        dim_val = getattr(
                                            datasets[dataset].config, dim
                                        ).values.get(code=row_dims[dim])
                                    else:
                                        dim_val = getattr(
                                            datasets[dataset].config, f"{dim}_surrogate"
                                        )

                                    dim_cache[row_dims[dim]][0].label = dim_val.label
                                    dim_cache[row_dims[dim]][0].save()
                                except DimensionValue.DoesNotExist:
                                    # Probably a code remapped from the SQL query
                                    pass

                        # Perform M2M association with indicator
                        getattr(
                            dims_cache["indicator"][row_dims["indicator"]][0],
                            dim_plurals[dim],  # Indicator has pluralized related name
                        ).add(dim_cache[row_dims[dim]][0])

                    dim_fields = {
                        dim: dims_cache[dim][row_dims[dim]][0] for dim in dims
                    }
                    fact_objects.append(
                        Fact(
                            value=value,
                            flags=flags,
                            **dim_fields,
                        )
                    )

                if fact_objects:
                    Fact.objects.bulk_create(fact_objects)
                    imported_count += len(fact_objects)

                progress.update(batch_task, advance=1)

        console.print(
            f"Imported facts: {imported_count} / {len(query_results)}",
        )

        # Report new instances based on the flag in the cached (<instance>, <created>) tuple.

        new_data_sources = [k for k, v in data_sources.items() if v[1]]
        if new_data_sources:
            console.print(f"[bold]New data sources[/]: {new_data_sources}")

        new_dim_values = {
            dim: [k for k, v in dims_cache[dim].items() if v[1]] for dim in dims
        }
        for dim in dims:
            if new_dim_values[dim]:
                console.print(f"[bold]New {dim} values[/]: {new_dim_values[dim]}")
