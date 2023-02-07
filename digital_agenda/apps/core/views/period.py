from rest_framework import viewsets
from django_filters import rest_framework as filters

from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.serializers import PeriodSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import FactFilterFilenameMixin


class PeriodViewSet(CodeLookupMixin, FactFilterFilenameMixin, viewsets.ReadOnlyModelViewSet):
    model = Period
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
