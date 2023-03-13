from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.common.admin import HasChangesAdminMixin


@admin.register(Chart)
class ChartAdmin(SortableAdminMixin, HasChangesAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {
        "code": (
            "chart_group",
            "name",
        ),
    }
    search_fields = ("code", "name", "description")
    list_filter = ("chart_group", "is_draft", "chart_type")
    list_select_related = ("chart_group",)
    list_display = (
        "display_order",
        "code",
        "chart_group",
        "name",
        "chart_type",
        "is_draft",
    )
    exclude = ("display_order",)
    autocomplete_fields = (
        "chart_group",
        *Chart.m2m_filter_options,
    )
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "is_draft",
                    "chart_group",
                    "name",
                    "code",
                    "chart_type",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Indicator Group Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "indicator_group_filter_hidden",
                    "indicator_group_filter_defaults",
                    "indicator_group_filter_ignored",
                ],
            },
        ),
        (
            "Indicator Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "indicator_filter_hidden",
                    "indicator_filter_defaults",
                    "indicator_filter_ignored",
                ],
            },
        ),
        (
            "Breakdown Group Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "breakdown_group_filter_hidden",
                    "breakdown_group_filter_defaults",
                    "breakdown_group_filter_ignored",
                ],
            },
        ),
        (
            "Breakdown Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "breakdown_filter_hidden",
                    "breakdown_filter_defaults",
                    "breakdown_filter_ignored",
                ],
            },
        ),
        (
            "Period Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "period_filter_hidden",
                    "period_filter_defaults",
                    "period_filter_ignored",
                ],
            },
        ),
        (
            "Unit Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "unit_filter_hidden",
                    "unit_filter_defaults",
                    "unit_filter_ignored",
                ],
            },
        ),
        (
            "Country Filter",
            {
                "classes": ["wide", "collapse"],
                "fields": [
                    "country_filter_hidden",
                    "country_filter_defaults",
                    "country_filter_ignored",
                ],
            },
        ),
        (
            "Advanced Settings",
            {
                "classes": ["collapse"],
                "fields": (
                    "min_value",
                    "max_value",
                ),
            },
        ),
    ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        result = super().formfield_for_manytomany(db_field, request, **kwargs)
        result.widget.attrs["style"] = "width: 580px;"
        return result


@admin.register(ChartGroup)
class ChartGroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ("code", "name", "short_name", "description")
    list_display = (
        "display_order",
        "code",
        "name",
        "short_name",
        "period_start",
        "period_end",
        "is_draft",
    )
    filter_horizontal = ("indicator_groups",)
