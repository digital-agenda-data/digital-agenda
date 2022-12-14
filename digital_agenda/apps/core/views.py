from django import forms
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Subquery
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
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
    BreakdownWithGroupsSerializer,
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
    period_in = CodeInFilter(field_name="periods__code", lookup_expr="in")

    class Meta(BaseCodeFilterSet.Meta):
        model = Indicator
        fields = BaseCodeFilterSet.Meta.fields + ["period_in"]


class IndicatorViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Indicator
    queryset = Indicator.objects.all().prefetch_related(
        "groups", "periods", "data_source"
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IndicatorCodeFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return IndicatorListSerializer

        return IndicatorDetailSerializer


class IndicatorGroupIndicatorViewSet(IndicatorViewSet):
    pagination_class = None

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(groups__code__in=[self.kwargs["indicator_group_code"]])
            .all()
        )

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
        return (
            super()
            .get_queryset()
            .filter(groups__code__in=[self.kwargs["breakdown_group_code"]])
            .all()
        )


class IndicatorFilteredMixin:
    """
    Mixin for queryset filtering based on indicator code URL param.
    Used for units/countries/periods.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(  # noqa
                indicators__code__in=[self.kwargs["indicator_code"]]  # noqa
            )
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
    pagination_class = None


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


class IndicatorBreakdownViewSet(IndicatorFilteredMixin, BreakdownViewSet):
    serializer_class = BreakdownWithGroupsSerializer
    queryset = Breakdown.objects.all().prefetch_related("groups")
    pagination_class = None


class IndicatorBreakdownGroupViewSet(BreakdownGroupViewSet):
    pagination_class = None

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Exists(
                    Breakdown.objects.filter(
                        groups__code__in=OuterRef("code"),
                        indicators__code__in=[self.kwargs["indicator_code"]],
                    )
                )
            )
        )


class IndicatorBreakdownGroupBreakdownViewSet(IndicatorFilteredMixin, BreakdownViewSet):
    pagination_class = None

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                groups__code__in=[self.kwargs["breakdown_group_code"]],
                indicators__code__in=[self.kwargs["indicator_code"]],
            )
        )


class DataSourceCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = DataSource


class DataSourceViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = DataSource
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DataSourceCodeFilterSet
    pagination_class = None


def filter_indicator_groups(queryset, name, value):
    return queryset.filter(
        indicator__id__in=Subquery(
            Indicator.objects.filter(groups__code=value).only("id")
        )
    )


def filter_breakdown_groups(queryset, name, value):
    return queryset.filter(
        breakdown__id__in=Subquery(
            Breakdown.objects.filter(groups__code=value).only("id")
        )
    )


class FactsFilter(filters.FilterSet):
    indicator_group = filters.CharFilter(
        field_name="indicator__code", method=filter_indicator_groups
    )
    indicator = filters.CharFilter(field_name="indicator__code")
    breakdown_group = filters.CharFilter(
        field_name="breakdown_code", method=filter_breakdown_groups
    )
    breakdown = filters.CharFilter(field_name="breakdown__code")
    unit = filters.CharFilter(field_name="unit__code", required=True)
    period = filters.CharFilter(field_name="period__code")
    country = filters.CharFilter(field_name="country__code")

    def get_form_class(self):
        # Ensure that at least one indicator and one breakdown filter
        # has been used to avoid accidentally making huge queries.

        def clean_indicator(form):
            data = form.cleaned_data
            if not data["indicator_group"] and not data["indicator"]:
                raise forms.ValidationError(
                    "Either indicator or indicator_group is required"
                )
            return data["indicator"]

        def clean_breakdown(form):
            data = form.cleaned_data
            if not data["breakdown_group"] and not data["breakdown"]:
                raise forms.ValidationError(
                    "Either breakdown or breakdown_group is required"
                )
            return data["breakdown"]

        form_class = super().get_form_class()
        form_class.clean_indicator = clean_indicator
        form_class.clean_breakdown = clean_breakdown

        return form_class

    class Meta:
        model = Fact
        fields = [
            "indicator_group",
            "indicator",
            "breakdown_group",
            "breakdown",
            "unit",
            "period",
            "country",
        ]


class FactsViewSet(CodeLookupMixin, ListModelMixin, viewsets.GenericViewSet):
    model = Fact
    serializer_class = CountryFactSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FactsFilter
    queryset = (
        Fact.objects.order_by(
            "period__code",
            "country__code",
            "indicator__code",
            "breakdown__code",
            "unit__code",
        )
        .filter(value__isnull=False)
        .select_related("country", "indicator", "breakdown", "period", "unit")
        .only(
            "country__code",
            "indicator__code",
            "breakdown__code",
            "period__code",
            "unit__code",
            "value",
            "flags",
        )
        .all()
    )
    pagination_class = None

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

