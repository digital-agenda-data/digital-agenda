import tempfile

from django.db import connection
from django.http import FileResponse


def export_facts_csv(
    filename, chart_group_id=None, indicator_group_id=None, indicator_id=None
):
    params = {
        "core_indicator": indicator_id,
        "core_indicatorgroup": indicator_group_id,
        "charts_chartgroup": chart_group_id,
    }

    filters = []
    for table, value in params.items():
        if not value:
            continue
        filters.append(f"{table}.id = %({table})s")

    assert filters, "At least one filter must be provided for export"

    query = f"""
        SELECT core_period.code    AS "period_code",
               core_indicator.code AS "indicator_code",
               core_breakdown.code AS "breakdown_code",
               core_unit.code      AS "unit_code",
               core_country.code   AS "country_code",
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
