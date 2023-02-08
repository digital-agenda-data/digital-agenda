from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action

from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import IndicatorGroup
from digital_agenda.apps.core.serializers import IndicatorGroupSerializer
from digital_agenda.apps.core.views import CodeLookupMixin
from digital_agenda.apps.core.views import ExistingFactFilterSet
from digital_agenda.apps.core.views import DimensionViewSetMixin
from digital_agenda.common.export import export_facts_csv


class IndicatorGroupFilterSet(ExistingFactFilterSet):
    fact_rel_name = "indicator__groups"


class IndicatorGroupViewSet(
    CodeLookupMixin, DimensionViewSetMixin, viewsets.ReadOnlyModelViewSet
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

    @action(methods=["GET"], detail=True)
    @method_decorator(never_cache)
    def facts(self, request, code=None):
        obj = self.get_object()
        return export_facts_csv(
            obj.code + "-data.csv",
            indicator_group_id=obj.id,
        )
