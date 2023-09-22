from datetime import date

from django.db.models import IntegerField
from django.db.models import Max
from django.db.models import Min
from django.db.models import Value
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
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.views import CodeLookupMixin
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
        obj = self.get_object()
        group_ids = obj.indicator_groups.all().values_list("id", flat=True)

        queryset = (
            Indicator.objects.filter(facts__period__isnull=False)
            .prefetch_related("data_sources")
            .annotate(
                period_start=Value(obj.period_start, IntegerField()),
                period_end=Value(obj.period_end, IntegerField()),
                fact_min_period=Min("facts__period__date"),
                fact_max_period=Max("facts__period__date"),
            )
            .filter(groups__id__in=group_ids)
        )

        if obj.period_start:
            queryset = queryset.exclude(
                fact_max_period__lt=date(obj.period_start, 1, 1)
            )
        if obj.period_end:
            queryset = queryset.exclude(
                fact_min_period__gt=date(obj.period_end, 12, 31)
            )

        return Response(ChartIndicatorListSerializer(queryset, many=True).data)


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
            .prefetch_related(*Chart.m2m_filter_options)
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
                   ts_rank(vector, query)       AS rank
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
