from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.serializers import BreakdownSerializer
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin


class BreakdownViewSet(DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    model = Breakdown
    serializer_class = BreakdownSerializer
    queryset = (
        Breakdown.objects.all()
        .select_related("chart_options")
        .order_by("breakdowngrouplink__display_order")
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        if breakdown_group_code := self.request.GET.get("breakdown_group"):
            # Filter links by breakdown group to avoid duplicates if a breakdown
            # belongs to multiple groups.
            # This can happen because the order of items is not global but is per group.
            qs = qs.filter(breakdowngrouplink__group__code=breakdown_group_code)
        return qs
