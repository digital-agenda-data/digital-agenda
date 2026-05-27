from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Unit
from digital_agenda.apps.core.serializers import UnitSerializer
from digital_agenda.apps.core.views import DimensionViewSetMixin, ExistingFactFilterSet


class UnitViewSet(DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    model = Unit
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
