from admin_auto_filters.filters import AutocompleteFilterFactory
from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib import messages
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.urls import reverse
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.widgets import ForeignKeyWidget

from digital_agenda.apps.charts.models import BreakdownChartOption
from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.charts.models import ExtraChartNote
from digital_agenda.apps.charts.models import ChartFontStyle
from digital_agenda.apps.charts.models import ChartFilterOrder
from digital_agenda.apps.charts.models import IndicatorChartOption
from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.common.admin import HasChangesAdminMixin


class ChartFilterOrderInline(SortableInlineAdminMixin, admin.StackedInline):
    extra = 0
    model = ChartFilterOrder


class ChartFontStyleInline(admin.TabularInline):
    extra = 0
    model = ChartFontStyle


@admin.register(Chart)
class ChartAdmin(SortableAdminMixin, HasChangesAdminMixin, admin.ModelAdmin):
    inlines = (
        ChartFontStyleInline,
        ChartFilterOrderInline,
    )
    prepopulated_fields = {"code": ("name",)}
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
    autocomplete_fields = ("chart_group", *Chart.get_m2m_filter_options())
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
        ("Chart Options", {"fields": ["legend_layout"]}),
        (
            "Chart Labels",
            {
                "description": (
                    "Chose what labels to use for each dimension in the charts. "
                    "This only applies to the chart itself and does not affect any "
                    "other location where the dimensions are displayed. "
                    "(filters, metadata page, etc.)"
                ),
                "classes": ["collapse"],
                "fields": [
                    "indicator_label",
                    "breakdown_label",
                    "period_label",
                    "unit_label",
                    "country_label",
                    "use_period_label_for_axis",
                ],
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
                    "indicator_group_filter_values",
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
                    "indicator_filter_values",
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
                    "breakdown_group_filter_values",
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
                    "breakdown_filter_values",
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
                    "period_filter_values",
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
                    "unit_filter_values",
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
                    "country_filter_values",
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
                    "min_year",
                    "max_year",
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
    actions = ["purge_data"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    @admin.action(description="Purge data for selected chart groups")
    def purge_data(self, request, queryset):
        return HttpResponseRedirect(
            reverse("admin:purge-facts")
            + "?ids="
            + ",".join(map(str, queryset.values_list("id", flat=True)))
        )

    def purge_data_view(self, request):
        opts = self.model._meta
        app_label = opts.app_label
        queryset = self.model.objects.filter(id__in=request.GET.get("ids").split(","))

        if request.method == "GET":
            return TemplateResponse(
                request,
                "admin/purge_facts_confirmation.html",
                context={
                    "opts": opts,
                    "app_label": app_label,
                    "queryset": queryset,
                    **self.admin_site.each_context(request),
                },
            )

        indicator_ids = list(
            Indicator.objects.filter(groups__chartgroup__in=queryset)
            .values_list("id", flat=True)
            .distinct()
        )

        try:
            with connection.cursor() as cursor:
                # We don't need any signals; all cascades ought to be at DB
                # level already. Avoid the excruciatingly slow ORM delete with
                # a simple SQL query.
                cursor.execute(
                    """
                        DELETE
                        FROM core_fact
                            WHERE core_fact.indicator_id = ANY(%s)
                    """,
                    (indicator_ids,),
                )
        finally:
            clear_all_caches(force=True)

        self.message_user(
            request,
            "Data has been deleted for the selected chart groups",
            level=messages.SUCCESS,
        )

        return redirect("admin:charts_chartgroup_changelist")

    def get_urls(self):
        return [
            path(
                "purge-facts/",
                self.admin_site.admin_view(self.purge_data_view),
                name="purge-facts",
            ),
            *super().get_urls(),
        ]


@admin.register(IndicatorChartOption)
class IndicatorChartOptionAdmin(admin.ModelAdmin):
    list_display = ("indicator", "color", "dash_style", "symbol", "custom_symbol")
    autocomplete_fields = ("indicator",)
    search_fields = ("indicator__code", "indicator__label", "indicator__alt_label")


@admin.register(BreakdownChartOption)
class BreakdownChartOptionAdmin(admin.ModelAdmin):
    list_display = ("breakdown", "color", "dash_style", "symbol", "custom_symbol")
    autocomplete_fields = ("breakdown",)
    search_fields = ("breakdown__code", "breakdown__label", "breakdown__alt_label")


class ExtraChartNoteResource(resources.ModelResource):
    indicator = resources.Field(
        column_name="indicator",
        attribute="indicator",
        widget=ForeignKeyWidget(Indicator, field="code"),
    )
    period = resources.Field(
        column_name="period",
        attribute="period",
        widget=ForeignKeyWidget(Period, field="code"),
    )

    class Meta:
        model = ExtraChartNote
        import_id_fields = ("indicator", "period")
        fields = ("indicator", "period", "note")


@admin.register(ExtraChartNote)
class ExtraChartNoteAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ExtraChartNoteResource
    list_display = ("indicator", "period", "note", "hide_from_line_charts")
    list_filter = (
        AutocompleteFilterFactory("indicator", "indicator"),
        AutocompleteFilterFactory("period", "period"),
        "hide_from_line_charts",
    )
    autocomplete_fields = ("indicator", "period")
    search_fields = (
        "indicator__code",
        "indicator__label",
        "indicator__alt_label",
        "period__code",
        "period__label",
        "period__alt_label",
        "note",
    )
