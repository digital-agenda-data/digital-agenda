from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action

from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.serializers import IndicatorListSerializer
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin
from digital_agenda.common.export import export_facts_csv


class IndicatorViewSet(DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    model = Indicator
    queryset = Indicator.objects.prefetch_related("data_sources")
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExistingFactFilterSet
    serializer_class = IndicatorListSerializer
    extra_headers = ["note", "data_sources"]

    @action(methods=["GET"], detail=True)
    @method_decorator(never_cache)
    def facts(self, request, code=None):
        obj = self.get_object()
        return export_facts_csv(
            obj.code + "-data.csv",
            indicator_id=obj.id,
        )
