from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from django_filters import rest_framework as filters


from .models import (
    IndicatorGroup,
    Indicator,
    BreakdownGroup,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)
from .serializers import (
    IndicatorGroupSerializer,
    IndicatorSerializer,
    BreakdownGroupSerializer,
    BreakdownSerializer,
    UnitSerializer,
    CountrySerializer,
    PeriodSerializer,
    CountryFactSerializer,
)


class CodeLookupMixin:
    lookup_field = "code"
    lookup_url_kwarg = "code"


class IndicatorGroupViewSet(viewsets.ReadOnlyModelViewSet, CodeLookupMixin):
    model = IndicatorGroup
    serializer_class = IndicatorGroupSerializer
    queryset = IndicatorGroup.objects.order_by("code").all()


class IndicatorViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Indicator
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.order_by("code").all()


class BreakdownGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = BreakdownGroup
    serializer_class = BreakdownGroupSerializer
    queryset = BreakdownGroup.objects.order_by("code").all()


class BreakdownViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Breakdown
    serializer_class = BreakdownSerializer
    queryset = Breakdown.objects.order_by("code").all()


class UnitViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Unit
    serializer_class = UnitSerializer
    queryset = Unit.objects.order_by("code").all()


class CountryViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Country
    serializer_class = CountrySerializer
    queryset = Country.objects.order_by("code").all()
    pagination_class = None

    def get_queryset(self):
        print(self.kwargs["indicator_code"])
        return self.model.objects.filter(
            indicators__code__in=[self.kwargs["indicator_code"]]
        )


class PeriodViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Period
    serializer_class = PeriodSerializer
    queryset = Period.objects.order_by("code").all()


class FactsPerCountryFilter(filters.FilterSet):

    indicator = filters.CharFilter(
        field_name="indicator__code", required=True  # lookup_expr="iexact",
    )
    breakdown = filters.CharFilter(
        field_name="breakdown__code", required=True  # lookup_expr="iexact",
    )
    unit = filters.CharFilter(
        field_name="unit__code", required=True  # lookup_expr="iexact",
    )
    period = filters.CharFilter(
        field_name="period__code", required=True  # lookup_expr="iexact",
    )

    class Meta:
        model = Fact
        fields = [
            "indicator",
            "breakdown",
            "unit",
            "period",
        ]


class FactsPerCountryViewSet(CodeLookupMixin, ListModelMixin, viewsets.GenericViewSet):
    model = Fact
    serializer_class = CountryFactSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FactsPerCountryFilter
    queryset = (
        Fact.objects.order_by("country__code")
        .select_related("country")
        .only("country__code", "value", "flags")
        .all()
    )
    pagination_class = None
