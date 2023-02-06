from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Subquery
from django_filters import rest_framework as filters
from rest_framework.decorators import action

from digital_agenda.apps.core.models import (
    Breakdown,
    BreakdownGroup,
    Country,
    DataSource,
    Fact,
    Indicator,
    IndicatorGroup,
    Period,
    Unit,
)
from digital_agenda.apps.core.serializers import (
    BreakdownGroupDetailSerializer,
    BreakdownGroupListSerializer,
    BreakdownSerializer,
    BreakdownWithGroupsSerializer,
    CountrySerializer,
    DataSourceSerializer,
    IndicatorDetailSerializer,
    IndicatorGroupDetailSerializer,
    IndicatorGroupListSerializer,
    IndicatorListSerializer,
    PeriodSerializer,
    UnitSerializer,
)
from digital_agenda.apps.core.views import CodeInFilter, CodeLookupMixin
from digital_agenda.apps.core.views import CustomXLSXFileMixin
from digital_agenda.common.export import export_facts_csv


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

    @action(methods=["GET"], detail=True)
    @method_decorator(never_cache)
    def facts(self, request, code=None):
        obj = self.get_object()
        return export_facts_csv(
            obj.code + "-data.csv",
            indicator_group_id=obj.id,
        )


class IndicatorCodeFilterSet(BaseCodeFilterSet):
    class Meta(BaseCodeFilterSet.Meta):
        model = Indicator
        fields = BaseCodeFilterSet.Meta.fields


class IndicatorViewSet(CodeLookupMixin, viewsets.ReadOnlyModelViewSet):
    model = Indicator
    queryset = Indicator.objects.exclude(facts__isnull=True).prefetch_related(
        "groups", "data_sources"
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IndicatorCodeFilterSet

    def get_serializer_class(self):
        if self.action == "list":
            return IndicatorListSerializer

        return IndicatorDetailSerializer

    @action(methods=["GET"], detail=True)
    @method_decorator(never_cache)
    def facts(self, request, code=None):
        obj = self.get_object()
        return export_facts_csv(
            obj.code + "-data.csv",
            indicator_id=obj.id,
        )


class IndicatorGroupIndicatorViewSet(IndicatorViewSet):
    pagination_class = None

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(groups__code__in=[self.kwargs["indicator_group_code"]])
            .order_by("indicatorgrouplink__display_order")
            .distinct("indicatorgrouplink__display_order", "code")
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
            .order_by("breakdowngrouplink__display_order")
            .distinct("breakdowngrouplink__display_order", "code")
        )


class IndicatorFilteredMixin(CustomXLSXFileMixin):
    """
    Mixin for queryset filtering based on indicator code URL param.
    Used for units/countries/periods.
    """

    filter_by = None

    def get_queryset(self):
        assert self.filter_by, "'filter_by' not provided"

        return (
            super()
            .get_queryset()
            .filter(
                id__in=Subquery(
                    Fact.objects.filter(indicator__code=self.kwargs["indicator_code"])
                    .distinct(self.filter_by)
                    .values_list(self.filter_by, flat=True)
                )
            )
        )

    def get_filename(self, request=None, *args, **kwargs):
        name = self.filter_by
        if self.filter_by.endswith("_id"):
            name = name[:-3]
        return self.kwargs["indicator_code"] + "_" + name + ".xlsx"


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
    filter_by = "unit_id"


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
    filter_by = "country_id"


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
    filter_by = "period_id"


class IndicatorBreakdownViewSet(IndicatorFilteredMixin, BreakdownViewSet):
    serializer_class = BreakdownWithGroupsSerializer
    queryset = Breakdown.objects.all().prefetch_related("groups")
    pagination_class = None
    filter_by = "breakdown_id"


class IndicatorBreakdownGroupViewSet(BreakdownGroupViewSet):
    pagination_class = None

    def get_queryset(self):
        breakdowns_for_indicator = Fact.objects.filter(
            indicator__code=self.kwargs["indicator_code"]
        ).values_list("breakdown_id", flat=True)
        return (
            super()
            .get_queryset()
            .filter(
                Exists(
                    Breakdown.objects.filter(
                        id__in=breakdowns_for_indicator,
                        groups__code__in=OuterRef("code"),
                    )
                )
            )
        )


class IndicatorBreakdownGroupBreakdownViewSet(IndicatorFilteredMixin, BreakdownViewSet):
    pagination_class = None
    filter_by = "breakdown_id"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                groups__code__in=[self.kwargs["breakdown_group_code"]],
            )
            .order_by("breakdowngrouplink__display_order")
            .distinct("breakdowngrouplink__display_order", "code")
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
