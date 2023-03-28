from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.serializers import BreakdownSerializer
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin


class BreakdownViewSet(DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    model = Breakdown
    serializer_class = BreakdownSerializer
    queryset = Breakdown.objects.all().order_by("breakdowngrouplink__display_order")
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
