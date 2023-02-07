from rest_framework import viewsets
from django_filters import rest_framework as filters

from digital_agenda.apps.core.models import Unit
from digital_agenda.apps.core.serializers import UnitSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import FactFilterFilenameMixin


class UnitViewSet(
    CodeLookupMixin, FactFilterFilenameMixin, viewsets.ReadOnlyModelViewSet
):
    model = Unit
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
