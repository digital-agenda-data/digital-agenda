from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.serializers import ChartGroupDetailSerializer
from digital_agenda.apps.charts.serializers import ChartGroupIndicatorSearchSerializer
from digital_agenda.apps.charts.serializers import ChartGroupListSerializer
from digital_agenda.apps.charts.serializers import ChartSerializer
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.serializers import IndicatorListSerializer
from digital_agenda.apps.core.serializers import IndicatorGroupListSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import IndicatorViewSet


class ChartGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = ChartGroup
    pagination_class = None

    def get_queryset(self):
        queryset = ChartGroup.objects.all().prefetch_related(
            "periods",
            "indicator_groups",
        )

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "indicator_groups__indicators",
                "indicator_groups__indicators__periods",
                "indicator_groups__indicators__groups",
                "indicator_groups__indicators__data_source",
            )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_draft=False)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ChartGroupListSerializer
        return ChartGroupDetailSerializer

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
        queryset = self.get_object().indicator_groups.all()
        return Response(IndicatorGroupListSerializer(queryset, many=True).data)

    @action(methods=["GET"], detail=True)
    def indicators(self, request, code=None):
        obj = self.get_object()
        group_ids = obj.indicator_groups.all().values_list("id", flat=True)
        period_ids = obj.periods.all().values_list("id", flat=True)

        queryset = IndicatorViewSet.queryset.filter(groups__id__in=group_ids)
        if period_ids:
            queryset = queryset.filter(periods__id__in=period_ids)

        return Response(IndicatorListSerializer(queryset, many=True).data)


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
            SELECT indicators.id            AS id,
                   indicators.code          AS code,
                   indicators.label         AS label,
                   indicators.alt_label     AS alt_label,
                   indicators.definition    AS definition,
                   indicator_groups.code    AS group_code,
                   chart_groups.code        AS chart_group_code,
                   highlight::json          AS highlight,
                   ts_rank(vector, query)   AS rank
            FROM indicators
                 INNER JOIN indicators_groups AS group_link
                            ON indicators.id = group_link.indicator_id
                 INNER JOIN indicator_groups
                            ON indicator_groups.id = group_link.group_id
                 INNER JOIN chart_groups_indicator_groups AS chart_group_link
                            ON indicator_groups.id = chart_group_link.indicatorgroup_id
                 INNER JOIN chart_groups
                            ON chart_group_link.chartgroup_id = chart_groups.id,
                 json_build_object(
                     'label', indicators.label,
                     'alt_label', indicators.alt_label,
                     'definition', indicators.definition
                 ) doc,
                 to_tsvector(%(config)s, doc) vector,
                 websearch_to_tsquery(%(config)s, %(query)s) query,
                 ts_headline(%(config)s, doc, query, %(options)s) highlight
             WHERE vector @@ query AND 
                   (%(is_auth)s OR chart_groups.is_draft = False)
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
