from rest_framework import viewsets

from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.serializers import ChartGroupDetailSerializer
from digital_agenda.apps.charts.serializers import ChartGroupListSerializer
from digital_agenda.apps.core.views import CodeLookupMixin


class ChartGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = ChartGroup
    pagination_class = None

    def get_queryset(self):
        queryset = ChartGroup.objects.all()
        if not self.request.user.is_authenticated:
            queryset.filter(is_draft=False)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ChartGroupListSerializer

        return ChartGroupDetailSerializer
