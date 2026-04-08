import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from digital_agenda.apps.core.models import CountryProfileIndicator
from digital_agenda.apps.core.models import CountryProfileIndicator
from digital_agenda.apps.core.serializers import CountryProfileIndicatorSerializer


class CountryProfileIndicatorFilterSet(django_filters.FilterSet):
    period = django_filters.CharFilter(field_name="period__code")

    class Meta:
        model = CountryProfileIndicator
        fields = ["period"]


class CountryProfileIndicatorViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = CountryProfileIndicator.objects.all().prefetch_related(
        "period",
        "indicator",
        "indicator_group",
        "indicator_group__parent",
        "indicator_group__indicators",
        "indicator_group__parent__indicators",
        "indicator__chart_options",
        "indicator__data_sources",
        "indicator__extra_notes",
        "indicator__extra_notes__period",
        "breakdown",
        "breakdown__chart_options",
        "unit",
    )
    serializer_class = CountryProfileIndicatorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryProfileIndicatorFilterSet
