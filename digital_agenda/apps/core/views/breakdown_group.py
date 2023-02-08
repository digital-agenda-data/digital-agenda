from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import BreakdownGroup
from digital_agenda.apps.core.serializers import BreakdownGroupSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin


class BreakdownGroupFilterSet(ExistingFactFilterSet):
    fact_rel_name = "breakdown__groups"


class BreakdownGroupViewSet(
    CodeLookupMixin, DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    model = BreakdownGroup
    queryset = BreakdownGroup.objects.all().prefetch_related(
        Prefetch(
            "breakdowns",
            Breakdown.objects.order_by("breakdowngrouplink__display_order"),
        )
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BreakdownGroupFilterSet
    serializer_class = BreakdownGroupSerializer
