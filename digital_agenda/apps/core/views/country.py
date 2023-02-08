from rest_framework import viewsets
from django_filters import rest_framework as filters

from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.serializers import CountrySerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin


class CountryViewSet(
    CodeLookupMixin, DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    model = Country
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
