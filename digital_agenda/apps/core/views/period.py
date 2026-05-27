from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.serializers import PeriodSerializer
from digital_agenda.apps.core.views import DimensionViewSetMixin, ExistingFactFilterSet


class PeriodViewSet(DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    model = Period
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
