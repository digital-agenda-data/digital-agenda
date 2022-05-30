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
        indicators = {}
        breakdowns = {}
        units = {}
        countries = {}
        periods = {}

        datasets = {}

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
                for row in results_batch:
                    (
                        estat_dataset,
                        indicator,
                        breakdown,
                        unit,
                        country,
                        period,
                        value,
                        flags,
                    ) = row

                    dataset = f"estat_{estat_dataset}"

                    # Datasets are kept as data source references
                    if dataset not in data_sources:
                        data_sources[dataset] = DataSource.objects.get_or_create(
                            code=dataset
                        )

                    if indicator not in indicators:
                        indicators[indicator] = Indicator.objects.update_or_create(
                            code=indicator,
                            defaults={
                                "data_source": data_sources[dataset][0],
                            },
                        )

                    if breakdown not in breakdowns:
                        breakdowns[breakdown] = Breakdown.objects.get_or_create(
                            code=breakdown
                        )
                    indicators[indicator][0].breakdowns.add(breakdowns[breakdown][0])

                    if dataset not in datasets:
                        datasets[dataset] = Dataset.objects.get(code=estat_dataset)

                    if unit not in units:
                        units[unit] = Unit.objects.get_or_create(code=unit)
                        if units[unit][1]:
                            if datasets[dataset].config.unit:
                                dim_val = datasets[dataset].config.unit.values.get(
                                    code=unit
                                )
                            else:
                                dim_val = datasets[dataset].config.unit_surrogate

                            units[unit][0].label = dim_val.label
                            units[unit][0].save()

                    indicators[indicator][0].units.add(units[unit][0])

                    if country not in countries:
                        countries[country] = Country.objects.get_or_create(code=country)
                        if countries[country][1]:
                            if datasets[dataset].config.country:
                                dim_val = datasets[dataset].config.country.values.get(
                                    code=country
                                )
                            else:
                                dim_val = datasets[dataset].config.country_surrogate

                            countries[country][0].label = dim_val.label
                            countries[country][0].save()

                    indicators[indicator][0].countries.add(countries[country][0])

                    if period not in periods:
                        periods[period] = Period.objects.get_or_create(code=period)
                    indicators[indicator][0].periods.add(periods[period][0])

                    fact_objects.append(
                        Fact(
                            value=value,
                            flags=flags,
                            indicator=indicators[indicator][0],
                            breakdown=breakdowns[breakdown][0],
                            unit=units[unit][0],
                            country=countries[country][0],
                            period=periods[period][0],
                        )
                    )

                if fact_objects:
                    Fact.objects.bulk_create(fact_objects)
                    imported_count += len(fact_objects)

                progress.update(batch_task, advance=1)

        console.print(
            f"Imported facts: {imported_count} / {len(query_results)}",
        )

        new_data_sources = [k for k, v in data_sources.items() if v[1]]
        new_indicators = [k for k, v in indicators.items() if v[1]]
        new_breakdowns = [k for k, v in breakdowns.items() if v[1]]
        new_units = [k for k, v in units.items() if v[1]]
        new_countries = [k for k, v in countries.items() if v[1]]
        new_periods = [k for k, v in periods.items() if v[1]]

        if new_data_sources:
            console.print(f"[bold]New data sources[/]: {new_data_sources}")

        if new_indicators:
            console.print(f"[bold]New indicators[/]: {new_indicators}")

        if new_breakdowns:
            console.print(f"[bold]New breakdowns[/]: {new_breakdowns}")

        if new_units:
            console.print(f"[bold]New units[/]: {new_units}")

        if new_countries:
            console.print(f"[bold]New countries[/]: {new_countries}")

        if new_periods:
            console.print(f"[bold]New periods[/]: {new_periods}")
