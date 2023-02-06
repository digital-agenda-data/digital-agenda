from django.db.models import Exists
from django.db.models import Max
from django.db.models import Min
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.serializers import ChartGroupIndicatorSearchSerializer
from digital_agenda.apps.charts.serializers import ChartGroupListSerializer
from digital_agenda.apps.charts.serializers import ChartIndicatorListSerializer
from digital_agenda.apps.charts.serializers import ChartSerializer
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.serializers import IndicatorGroupDetailSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.common.export import export_facts_csv


class ChartGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = ChartGroup
    pagination_class = None
    serializer_class = ChartGroupListSerializer

    def get_queryset(self):
        queryset = ChartGroup.objects.all().prefetch_related(
            "indicator_groups",
        )

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

    @action(
        methods=["GET"],
        detail=True,
        url_path="indicator-groups",
        url_name="indicator-groups",
    )
    def indicator_groups(self, request, code=None):
        queryset = (
            self.get_object()
            .indicator_groups.all()
            .filter(Exists(Fact.objects.filter(indicator__groups__id=OuterRef("id"))))
            .prefetch_related(
                Prefetch(
                    "indicators",
                    Indicator.objects.order_by("indicatorgrouplink__display_order"),
                ),
                "indicators__groups",
                "indicators__data_sources",
            )
        )
        return Response(IndicatorGroupDetailSerializer(queryset, many=True).data)

    @action(methods=["GET"], detail=True)
    def indicators(self, request, code=None):
        obj = self.get_object()
        group_ids = obj.indicator_groups.all().values_list("id", flat=True)

        queryset = (
            Indicator.objects.filter(facts__period__isnull=False)
            .annotate(
                min_period=Min("facts__period__code"),
                max_period=Max("facts__period__code"),
            )
            .filter(groups__id__in=group_ids)
            .prefetch_related("groups", "data_sources")
        )

        if obj.period_start:
            queryset = queryset.exclude(max_period__lt=obj.period_start)
        if obj.period_end:
            queryset = queryset.exclude(min_period__gt=obj.period_end)

        return Response(ChartIndicatorListSerializer(queryset, many=True).data)

    @action(methods=["GET"], detail=True)
    @method_decorator(never_cache)
    def facts(self, request, code=None):
        obj = self.get_object()
        return export_facts_csv(
            obj.short_name + "-data.csv",
            chart_group_id=obj.id,
        )


class ChartViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Chart
    pagination_class = None
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
