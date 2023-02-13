from rest_framework import viewsets
from django_filters import rest_framework as filters

from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.serializers import IndicatorListSerializer
from digital_agenda.apps.core.views import DimensionViewSetMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.common.export import FactExportMixin


class IndicatorViewSet(
    FactExportMixin, DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    model = Indicator
    queryset = Indicator.objects.prefetch_related("data_sources")
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
    serializer_class = IndicatorListSerializer
    extra_headers = ["note", "data_sources"]