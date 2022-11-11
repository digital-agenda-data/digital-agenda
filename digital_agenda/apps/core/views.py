from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin

from django_filters import rest_framework as filters


from .models import (
    IndicatorGroup,
    Indicator,
    DataSource,
    BreakdownGroup,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)
from .serializers import (
    IndicatorGroupListSerializer,
    IndicatorGroupDetailSerializer,
    IndicatorListSerializer,
    IndicatorDetailSerializer,
    BreakdownGroupListSerializer,
    BreakdownGroupDetailSerializer,
    BreakdownSerializer,
    UnitSerializer,
    CountrySerializer,
    PeriodSerializer,
    CountryFactSerializer,
    DataSourceSerializer,
)


class CodeLookupMixin:
    lookup_field = "code"
    lookup_url_kwarg = "code"


class CodeInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BaseCodeFilterSet(filters.FilterSet):
    code_in = CodeInFilter(field_name="code", lookup_expr="in")

    class Meta:
        fields = ["code_in"]


class IndicatorGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = IndicatorGroup
    queryset = IndicatorGroup.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return IndicatorGroupListSerializer

        return IndicatorGroupDetailSerializer


class IndicatorCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = Indicator


class IndicatorViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Indicator
    queryset = Indicator.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IndicatorCodeFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return IndicatorListSerializer

        return IndicatorDetailSerializer


class IndicatorGroupIndicatorViewSet(IndicatorViewSet):
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            groups__code__in=[self.kwargs["indicator_group_code"]]
        ).all()

    def get_serializer_class(self):
        if self.action == "list":
            return IndicatorListSerializer

        return IndicatorDetailSerializer


class BreakdownGroupViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = BreakdownGroup
    queryset = BreakdownGroup.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return BreakdownGroupListSerializer

        return BreakdownGroupDetailSerializer


class BreakdownCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = Breakdown


class BreakdownViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Breakdown
    serializer_class = BreakdownSerializer
    queryset = Breakdown.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BreakdownCodeFilterSet


class BreakdownGroupBreakdownViewSet(BreakdownViewSet):
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(
            groups__code__in=[self.kwargs["breakdown_group_code"]]
        ).all()


class IndicatorFilteredMixin:
    """
    Mixin for queryset filtering based on indicator code URL param.
    Used for units/countries/periods.
    """

    def get_queryset(self):
        return self.model.objects.filter(  # noqa
            indicators__code__in=[self.kwargs["indicator_code"]]  # noqa
        )


class UnitCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = Unit


class UnitViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Unit
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UnitCodeFilterSet


class IndicatorUnitViewSet(IndicatorFilteredMixin, UnitViewSet):
    pagination_class = None


class CountryCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = Country


class CountryViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Country
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CountryCodeFilterSet


class IndicatorCountryViewSet(IndicatorFilteredMixin, CountryViewSet):
    pagination_class = None


class PeriodCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = Period


class PeriodViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Period
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PeriodCodeFilterSet


class IndicatorPeriodViewSet(IndicatorFilteredMixin, PeriodViewSet):
    pagination_class = None


class DataSourceCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = DataSource


class DataSourceViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = DataSource
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DataSourceCodeFilterSet


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
