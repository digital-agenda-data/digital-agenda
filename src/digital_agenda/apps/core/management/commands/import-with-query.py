import math

from django.core.management.base import BaseCommand
from django.db import connection

from django_sql_dashboard.models import DashboardQuery

from rich.progress import Progress
from rich.console import Console

from digital_agenda.apps.core.models import (
    DataSource,
    DataSourceReference,
    Indicator,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)

console = Console()


class Command(BaseCommand):
    help = "Run an import based on a dashboard-stored query"

    def add_arguments(self, parser):
        parser.add_argument(
            "data_source", type=str.lower, help="Data source (e.g. ESTAT)"
        )
        parser.add_argument("dashboard_slug", type=str.lower, help="Dashboard slug")
        parser.add_argument("--batch-size", type=int, default=1000, help="Batch size")

    def handle(
        self,
        data_source,
        dashboard_slug,
        batch_size,
        *args,
        **options,
    ):
        try:
            datasource = DataSource.objects.get(name__iexact=data_source)
        except DataSource.DoesNotExist:
            console.print(f"[red]Data source not found: {data_source}.")
            exit(1)

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

        # Object instance caches, indexed by dimension values in the query results
        data_source_refs = {}
        indicators = {}
        breakdowns = {}
        units = {}
        countries = {}
        periods = {}

        batches = math.ceil(len(query_results) / batch_size)
        imported_count = 0

        with Progress() as progress:
            batch_task = progress.add_task(
                f"[green]Importing {data_source} facts for dashboard query {dashboard_slug}",
                total=batches,
            )
            for i in range(0, len(query_results), batch_size):
                results_batch = query_results[i : i + batch_size]
                fact_objects = []
                for row in results_batch:
                    (
                        dataset,
                        indicator,
                        breakdown,
                        unit,
                        country,
                        period,
                        value,
                        flags,
                    ) = row

                    # Datasets are kept as data source references
                    if dataset not in data_source_refs:
                        (
                            data_source_refs[dataset],
                            _,
                        ) = DataSourceReference.objects.get_or_create(
                            data_source=datasource, name=dataset
                        )

                    if indicator not in indicators:
                        indicators[indicator], _ = Indicator.objects.get_or_create(
                            data_source_ref=data_source_refs[dataset],
                            code=indicator,
                        )
                        if (
                            indicators[indicator].data_source_ref
                            != data_source_refs[dataset]
                        ):
                            console.print(
                                "[red]Aborting import = duplicated indicator in datasets"
                                f" {indicators[indicator].data_source_ref} / {data_source_refs[dataset]}",
                                new_line_start=True,
                            )
                            exit(1)

                    if breakdown not in breakdowns:
                        breakdowns[breakdown], _ = Breakdown.objects.get_or_create(
                            code=breakdown
                        )
                    indicators[indicator].breakdowns.add(breakdowns[breakdown])

                    if unit not in units:
                        units[unit], _ = Unit.objects.get_or_create(code=unit)
                    indicators[indicator].units.add(units[unit])

                    if country not in countries:
                        countries[country], _ = Country.objects.get_or_create(
                            code=country
                        )
                    indicators[indicator].countries.add(countries[country])

                    if period not in periods:
                        periods[period], _ = Period.objects.get_or_create(code=period)
                    indicators[indicator].periods.add(periods[period])

                    fact_objects.append(
                        Fact(
                            value=value,
                            flags=flags,
                            indicator=indicators[indicator],
                            breakdown=breakdowns[breakdown],
                            unit=units[unit],
                            country=countries[country],
                            period=periods[period],
                        )
                    )

                if fact_objects:
                    Fact.objects.bulk_create(fact_objects)
                    imported_count += len(fact_objects)

                progress.update(batch_task, advance=1)

        console.print(
            f"Imported facts: {imported_count} / {len(query_results)}",
        )
