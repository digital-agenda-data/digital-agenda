from rest_framework import viewsets

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.serializers import ChartGroupDetailSerializer
from digital_agenda.apps.charts.serializers import ChartGroupListSerializer
from digital_agenda.apps.charts.serializers import ChartSerializer
from digital_agenda.apps.core.views import CodeLookupMixin


class ChartGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = ChartGroup
    pagination_class = None

    def get_queryset(self):
        queryset = ChartGroup.objects.all().prefetch_related(
            "indicator_groups",
            "indicator_groups__indicators",
            "indicator_groups__indicators__periods",
            "indicator_groups__indicators__data_source",
        )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_draft=False)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ChartGroupListSerializer
        return ChartGroupDetailSerializer


class ChartViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Chart
    pagination_class = None
    serializer_class = ChartSerializer

    def get_queryset(self):
        queryset = ChartGroup.objects.all().prefetch_related(
            "chart_group",
        )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_draft=False)
        return queryset
