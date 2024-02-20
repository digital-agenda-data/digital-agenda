from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import OuterRef
from django.db.models import Subquery
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.serializers.chart import ChartIndicatorListSerializer
from digital_agenda.apps.charts.serializers.chart import ChartSerializer
from digital_agenda.apps.charts.serializers.chart_group import (
    ChartGroupIndicatorSearchSerializer,
)
from digital_agenda.apps.charts.serializers.chart_group import ChartGroupSerializer
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views.facts import FactsViewSet
from digital_agenda.common.export import FactExportMixin


class ChartGroupViewSet(
    FactExportMixin, CodeLookupMixin, viewsets.ReadOnlyModelViewSet
):
    model = ChartGroup

    def get_queryset(self):
        queryset = ChartGroup.objects.all().prefetch_related("indicator_groups")

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_draft=False)
        return queryset

    # Must Vary on cookies since the list changes if the user
    # is logged in or not
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "indicators":
            return ChartIndicatorListSerializer
        return ChartGroupSerializer

    @action(methods=["GET"], detail=True)
    def indicators(self, request, code=None):
        """Get indicators and min/max periods for this chart group"""
        chart_group = self.get_object()
        end_date = chart_group.period_end_date
        start_date = chart_group.period_start_date

        fact_subquery = Fact.objects.filter(indicator_id=OuterRef("id")).order_by(
            "-period__date"
        )
        if start_date:
            fact_subquery = fact_subquery.filter(period__date__gte=start_date)
        if end_date:
            fact_subquery = fact_subquery.filter(period__date__lte=end_date)

        group_ids = chart_group.indicator_groups.all().values_list("id", flat=True)
        indicators = list(
            Indicator.objects.filter(facts__period__isnull=False)
            .prefetch_related("data_sources")
            .annotate(
                # Fetch all periods to correctly compute the "time coverage",
                # including any gaps in the data.
                period_ids=ArrayAgg("facts__period_id", distinct=True),
                # Fetch one sample fact to have all necessary details to compute a
                # valid link to a chart showing this indicator.
                sample_fact_id=Subquery(fact_subquery.values("id")[:1]),
            )
            .filter(groups__id__in=group_ids)
        )

        # Prefetch all required objects in bulk
        period_by_ids = Period.objects.in_bulk(
            {
                period_id
                for indicator in indicators
                for period_id in indicator.period_ids
            }
        )
        facts_by_id = FactsViewSet.queryset.in_bulk(
            {indicator.sample_fact_id for indicator in indicators}
        )

        results = []
        for indicator in indicators:
            indicator.sample_fact = facts_by_id[indicator.sample_fact_id]

            all_periods = []
            for period_id in indicator.period_ids:
                period = period_by_ids[period_id]
                # Filter out any periods that are not included the chart group
                # configured period interval
                if start_date and period.date < start_date:
                    continue
                if end_date and period.date > end_date:
                    continue
                all_periods.append(period)

            if not all_periods:
                # Indicator has no facts in the chart group period range
                continue

            all_periods.sort(key=lambda p: p.date)
            indicator.all_periods = all_periods
            indicator.min_period = all_periods[0]
            indicator.max_period = all_periods[-1]
            results.append(indicator)

        return Response(ChartIndicatorListSerializer(results, many=True).data)


class ChartViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Chart
    serializer_class = ChartSerializer

    # Must Vary on cookies since the list changes if the user
    # is logged in or not
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        queryset = (
            Chart.objects.all()
            .select_related("chart_group")
            .prefetch_related("filter_order", *Chart.m2m_filter_options)
        )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_draft=False)

        return queryset


class ChartGroupIndicatorSearchViewSet(
    viewsets.mixins.ListModelMixin, viewsets.GenericViewSet
):
    model = Indicator
    serializer_class = ChartGroupIndicatorSearchSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        # XXX A braver soul than I can attempt to use the ORM to write a similar
        # XXX query that correctly creates a cartesian product and handles full text
        # XXX search AND ranking results. Good luck!
        # Intentional cartesian product. An indicator can have many
        # groups that can belong to many chart groups.
        # Any orphaned indicators are excluded from the search.
        query = """
            SELECT core_indicator.id            AS id,
                   core_indicator.code          AS code,
                   core_indicator.label         AS label,
                   core_indicator.alt_label     AS alt_label,
                   core_indicator.definition    AS definition,
                   core_indicatorgroup.code     AS group_code,
                   charts_chartgroup.code       AS chart_group_code,
                   highlight::json              AS highlight,
                   ts_rank(vector, query)       AS rank,
                   -- Fetch one sample fact to have all necessary details to compute a 
                   -- valid link to a chart showing this indicator.
                   (SELECT core_fact.id
                    FROM core_fact
                         INNER JOIN core_period
                                    ON (core_period.id = core_fact.period_id)
                    WHERE indicator_id = core_indicator.id
                      AND (
                        charts_chartgroup.period_start IS NULL OR
                        EXTRACT(YEAR FROM core_period.date) >= charts_chartgroup.period_start
                        )
                      AND (
                        charts_chartgroup.period_end IS NULL OR
                        EXTRACT(YEAR FROM core_period.date) <= charts_chartgroup.period_end
                        )
                    ORDER BY core_period.date DESC
                    LIMIT 1)                    AS sample_fact_id
            FROM core_indicator
                 INNER JOIN core_indicatorgrouplink
                            ON core_indicator.id = core_indicatorgrouplink.indicator_id
                 INNER JOIN core_indicatorgroup
                            ON core_indicatorgroup.id = core_indicatorgrouplink.group_id
                 INNER JOIN charts_chartgroup_indicator_groups
                            ON core_indicatorgroup.id = charts_chartgroup_indicator_groups.indicatorgroup_id
                 INNER JOIN charts_chartgroup
                            ON charts_chartgroup_indicator_groups.chartgroup_id = charts_chartgroup.id,
                 json_build_object(
                     'code', core_indicator.code,
                     'label', core_indicator.label,
                     'alt_label', core_indicator.alt_label,
                     'definition', core_indicator.definition
                 ) doc,
                 to_tsvector(%(config)s, doc) vector,
                 websearch_to_tsquery(%(config)s, %(query)s) query,
                 ts_headline(%(config)s, doc, query, %(options)s) highlight
             WHERE vector @@ query AND 
                   -- Hide draft chart groups for non-auth users 
                   (%(is_auth)s OR charts_chartgroup.is_draft = False) AND 
                   -- Only show indicators that have data
                   EXISTS(
                        SELECT 1 
                        FROM core_fact 
                        WHERE core_fact.indicator_id = core_indicator.id
                   )
             ORDER BY rank DESC
        """

        return Indicator.objects.raw(
            query,
            params={
                "config": "english",
                "query": self.request.GET.get("search"),
                "is_auth": self.request.user.is_authenticated,
                # See available options here
                # https://www.postgresql.org/docs/current/textsearch-controls.html#TEXTSEARCH-HEADLINE
                "options": "HighlightAll=true",
            },
        )

    # Likely to have a lot of cache misses, does not seem worth caching.
    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer(self, queryset, *args, **kwargs):
        indicators = list(queryset)

        facts_by_id = FactsViewSet.queryset.in_bulk(
            {indicator.sample_fact_id for indicator in indicators}
        )
        for indicator in indicators:
            indicator.sample_fact = facts_by_id[indicator.sample_fact_id]

        return super().get_serializer(indicators, *args, **kwargs)
