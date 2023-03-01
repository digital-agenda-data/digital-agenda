import tempfile

from django.db import connection
from django.http import FileResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.decorators import action
from rest_framework_csv.renderers import CSVRenderer

from digital_agenda.apps.core.serializers import FactSerializer


class FactExportMixin:
    def get_serializer_class(self):
        if self.action == "facts":
            return FactSerializer
        return super().get_serializer_class()

    def get_renderers(self):
        if self.action == "facts":
            return [CSVRenderer]
        return super().get_renderers()

    @action(methods=["GET"], detail=True)
    @method_decorator(never_cache)
    def facts(self, request, code=None):
        """Optimized bulk export for facts. Only support CSV format."""
        return export_facts_csv(
            code + "-data.csv",
            **{
                self.model._meta.model_name: self.get_object().id,
            },
        )


def export_facts_csv(filename, chartgroup=None, indicatorgroup=None, indicator=None):
    """Optimized fact export for large dataset. MUCH faster as it bypasses
    python altogether.
    """
    params = {
        "core_indicator": indicator,
        "core_indicatorgroup": indicatorgroup,
        "charts_chartgroup": chartgroup,
    }

    filters = []
    for table, value in params.items():
        if not value:
            continue
        filters.append(f"{table}.id = %({table})s")

    assert filters, "At least one filter must be provided for export"

    query = f"""
        SELECT core_period.code    AS "period",
               core_country.code   AS "country",
               core_indicator.code AS "indicator",
               core_breakdown.code AS "breakdown",
               core_unit.code      AS "unit",
               core_fact.value     AS "value",
               core_fact.flags     AS "flags"
        FROM core_fact
                 INNER JOIN core_indicator
                            ON (core_fact.indicator_id = core_indicator.id)
                 INNER JOIN core_breakdown
                            ON (core_fact.breakdown_id = core_breakdown.id)
                 INNER JOIN core_unit
                            ON (core_fact.unit_id = core_unit.id)
                 INNER JOIN core_country
                            ON (core_fact.country_id = core_country.id)
                 INNER JOIN core_period
                            ON (core_fact.period_id = core_period.id)
        WHERE EXISTS(
          SELECT 1
          FROM charts_chartgroup
                 INNER JOIN charts_chartgroup_indicator_groups
                            ON charts_chartgroup.id = charts_chartgroup_indicator_groups.chartgroup_id
                 INNER JOIN core_indicatorgroup
                            ON charts_chartgroup_indicator_groups.indicatorgroup_id = core_indicatorgroup.id
                 INNER JOIN core_indicatorgrouplink
                            ON (core_indicatorgroup.id = core_indicatorgrouplink.group_id AND
                                core_indicatorgrouplink.indicator_id = core_indicator.id)
          WHERE {" AND ".join(filters)}  
        )    
    """

    # FileResponse will automatically close this file (and hence be removed)
    tmpf = tempfile.NamedTemporaryFile(prefix="chart-group-export-", mode="wb+")

    try:
        with connection.cursor() as cursor:
            query_interpolated = cursor.mogrify(
                f"COPY ({query}) TO STDOUT WITH CSV HEADER",
                params,
            )
            cursor.copy_expert(query_interpolated, tmpf)

            tmpf.seek(0)
            return FileResponse(tmpf, as_attachment=True, filename=filename)
    except Exception:
        # Close file in case of errors since FileResponse probably won't get
        # to do it for us.
        tmpf.close()
        raise
