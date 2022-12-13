from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.serializers import ChartGroupDetailSerializer
from digital_agenda.apps.charts.serializers import ChartGroupListSerializer
from digital_agenda.apps.charts.serializers import ChartSerializer
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

    def get_queryset(self):
        queryset = (
            Chart.objects.all()
            .select_related("chart_group")
            .prefetch_related(
                "indicator_group_filter_defaults",
                "indicator_group_filter_ignored",
                "indicator_filter_defaults",
                "indicator_filter_ignored",
                "breakdown_group_filter_defaults",
                "breakdown_group_filter_ignored",
                "breakdown_filter_defaults",
                "breakdown_filter_ignored",
                "period_filter_defaults",
                "period_filter_ignored",
                "unit_filter_defaults",
                "unit_filter_ignored",
                "country_filter_defaults",
                "country_filter_ignored",
            )
        )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_draft=False)

        return queryset
