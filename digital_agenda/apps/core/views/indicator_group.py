from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import IndicatorGroup
from digital_agenda.apps.core.serializers import IndicatorGroupSerializer
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin
from digital_agenda.common.export import FactExportMixin


class IndicatorGroupFilterSet(ExistingFactFilterSet):
    fact_rel_name = "indicator__groups"


class IndicatorGroupViewSet(
    FactExportMixin, DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    model = IndicatorGroup
    queryset = IndicatorGroup.objects.all().prefetch_related(
        Prefetch(
            "indicators",
            Indicator.objects.order_by("indicatorgrouplink__display_order"),
        )
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IndicatorGroupFilterSet
    serializer_class = IndicatorGroupSerializer
