from django_filters import rest_framework as filters
from rest_framework import viewsets

from digital_agenda.apps.core.models import DataSource
from digital_agenda.apps.core.serializers import DataSourceSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin


class DataSourceFilterSet(ExistingFactFilterSet):
    fact_rel_name = "indicator__data_sources"


class DataSourceViewSet(
    CodeLookupMixin, DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    model = DataSource
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DataSourceFilterSet
    extra_headers = ["note", "url"]
