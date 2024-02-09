from django.db.models import Exists
from django.db.models import OuterRef
from django.utils.encoding import force_str
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
        label="unit.code",
        help_text="Filter results by unit code",
    )
    period = filters.CharFilter(
        field_name="period__code",
        label="period.code",
        help_text="Filter results by period code",
    )
    country = filters.CharFilter(
        field_name="country__code",
        label="country.code",
        help_text="Filter results by country code",
    )
    indicator = filters.CharFilter(
        field_name="indicator__code",
        label="indicator.code",
        help_text="Filter results by indicator code",
    )
    breakdown = filters.CharFilter(
        field_name="breakdown__code",
        label="breakdown.code",
        help_text="Filter results by breakdown code",
    )
    data_source = filters.CharFilter(
        field_name="indicator__data_sources__code",
        label="data_source.code",
        help_text="Filter results by data_source code",
    )
    indicator_group = filters.CharFilter(
        field_name="indicator__groups__code",
        label="indicator_group.code",
        help_text="Filter results by indicator_group code",
    )
    breakdown_group = filters.CharFilter(
        field_name="breakdown__groups__code",
        label="breakdown_group.code",
        help_text="Filter results by breakdown_group code",
    )
    chart_group = filters.CharFilter(
        field_name="indicator__groups__chartgroup__code",
        label="chart_group.code",
        help_text="Filter results by chart_group code",
    )

    def get_rel_name(self, queryset):
        return self.fact_rel_name or queryset.model.facts.field.name

    def filter_queryset(self, queryset):
        # All the filters actually apply to the facts, and we simply filter by a
        # subquery referencing on fact with an outer reference to the model.
        fact_qs = super().filter_queryset(Fact.objects.all())

        rel_name = self.get_rel_name(queryset)
        return queryset.filter(
            Exists(
                fact_qs.filter(
                    **{
                        rel_name: OuterRef("pk"),
                    }
                )
            )
        )


class DimensionViewSetMixin(CodeLookupMixin, FilenameExportMixin):
    extra_headers = []

    def get_renderer_context(self):
        return {
            **super().get_renderer_context(),
            "header": ["code", "label", "alt_label", "definition"] + self.extra_headers,
        }

    def get_filename(self, request, *args, **kwargs):
        filters = []
        for key in self.filterset_class.base_filters:
            if value := request.GET.get(key):
                filters.append(force_str(value))
        filters.append(force_str(self.model._meta.verbose_name_plural))

        return "-".join(filters)
