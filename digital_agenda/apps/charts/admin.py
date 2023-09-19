from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.contrib import messages
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.urls import reverse

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.cache import clear_all_caches
from digital_agenda.apps.core.models import Indicator
from digital_agenda.common.admin import HasChangesAdminMixin


@admin.register(Chart)
class ChartAdmin(SortableAdminMixin, HasChangesAdminMixin, admin.ModelAdmin):
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
    autocomplete_fields = ("chart_group", *Chart.m2m_filter_options)
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
            {"classes": ["collapse"], "fields": ("min_value", "max_value")},
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
