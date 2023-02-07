from django.db.models import Exists
from django.db.models import OuterRef
from django_filters import rest_framework as filters

from digital_agenda.apps.core.models import Fact
from digital_agenda.common.viewset import FilenameExportMixin


class CodeLookupMixin:
    lookup_field = "code"
    lookup_url_kwarg = "code"


class CodeInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ExistingFactFilterSet(filters.FilterSet):
    fact_rel_name = None
    unit = filters.CharFilter(
        field_name="unit__code",
        label="unit",
        method="filter_existing_fact",
    )
    period = filters.CharFilter(
        field_name="period__code",
        label="period",
        method="filter_existing_fact",
    )
    country = filters.CharFilter(
        field_name="country__code",
        label="country",
        method="filter_existing_fact",
    )
    indicator = filters.CharFilter(
        field_name="indicator__code",
        label="indicator",
        method="filter_existing_fact",
    )
    breakdown = filters.CharFilter(
        field_name="breakdown__code",
        label="breakdown",
        method="filter_existing_fact",
    )
    data_source = filters.CharFilter(
        field_name="indicator__data_sources__code",
        label="data_source",
        method="filter_existing_fact",
    )
    indicator_group = filters.CharFilter(
        field_name="indicator__groups__code",
        label="indicator_group",
        method="filter_existing_fact",
    )
    breakdown_group = filters.CharFilter(
        field_name="breakdown__groups__code",
        label="breakdown_group",
        method="filter_existing_fact",
    )
    chart_group = filters.CharFilter(
        field_name="indicator__groups__chartgroup__code",
        label="chart_group",
        method="filter_existing_fact",
    )

    def get_rel_name(self, queryset):
        return self.fact_rel_name or queryset.model.facts.field.name

    def filter_existing_fact(self, queryset, name, value):
        rel_name = self.get_rel_name(queryset)

        return queryset.filter(
            Exists(
                Fact.objects.filter(
                    **{
                        name: value,
                        rel_name: OuterRef("pk"),
                    }
                )
            )
        )


class FactFilterFilenameMixin(FilenameExportMixin):
    def get_filename(self, request, *args, **kwargs):
        filters = []
        for key in ExistingFactFilterSet.base_filters:
            if value := request.GET.get(key):
                filters.append(value)
        filters.append(self.model._meta.verbose_name_plural)

        return "-".join(filters) + ".csv"
