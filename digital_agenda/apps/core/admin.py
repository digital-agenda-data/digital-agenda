import json

from django.contrib import admin, messages
from django.db import models

from admin_auto_filters.filters import AutocompleteFilter
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget
from django_task.admin import TaskAdmin

from .models import (
    DataSource,
    IndicatorGroup,
    Indicator,
    BreakdownGroup,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
    DataFileImport,
    DataFileImportTask,
)


class DimensionAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    list_per_page = 20


admin.site.register(DataSource, DimensionAdmin)


class SortableDimensionAdmin(SortableAdminMixin, DimensionAdmin):
    pass


class IndicatorTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    model = IndicatorGroup.indicators.through


class IndicatorsFilter(AutocompleteFilter):
    title = "Indicator"
    field_name = "indicators"


@admin.register(IndicatorGroup)
class IndicatorGroupAdmin(SortableDimensionAdmin):
    inlines = (IndicatorTabularInline,)
    list_filter = [IndicatorsFilter]


class DataSourceFilter(AutocompleteFilter):
    title = "Data Source"
    field_name = "data_sources"


class DataSourceInline(admin.TabularInline):
    model = Indicator.data_sources.through
    extra = 0


@admin.register(Indicator)
class IndicatorAdmin(DimensionAdmin):
    list_filter = [DataSourceFilter]
    inlines = (DataSourceInline,)


class BreakdownTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    model = BreakdownGroup.breakdowns.through


class BreakdownsFilter(AutocompleteFilter):
    title = "Breakdown"
    field_name = "breakdowns"


@admin.register(BreakdownGroup)
class BreakdownGroupAdmin(SortableDimensionAdmin):
    inlines = (BreakdownTabularInline,)
    list_filter = [BreakdownsFilter]


admin.site.register(Breakdown, DimensionAdmin)

admin.site.register(Unit, DimensionAdmin)

admin.site.register(Period, DimensionAdmin)


@admin.register(Country)
class CountryAdmin(DimensionAdmin):
    list_display = ("code", "is_group", "label", "alt_label", "color")
    list_filter = ("is_group",)


class IndicatorFilter(AutocompleteFilter):
    title = "Indicator"
    field_name = "indicator"


class CountryFilter(AutocompleteFilter):
    title = "Country"
    field_name = "country"


class PeriodFilter(AutocompleteFilter):
    title = "Period"
    field_name = "period"


class ImportConfigFilter(AutocompleteFilter):
    title = "Import Config"
    field_name = "import_config"


class ImportFileFilter(AutocompleteFilter):
    title = "Import File"
    field_name = "import_file"


class FactAdmin(admin.ModelAdmin):
    list_display = (
        "indicator",
        "breakdown",
        "unit",
        "country",
        "period",
        "value",
        "flags",
        "import_config",
        "import_file",
    )
    list_filter = [
        ImportConfigFilter,
        ImportFileFilter,
        IndicatorFilter,
        CountryFilter,
        PeriodFilter,
    ]
    list_per_page = 50
    autocomplete_fields = (
        "indicator",
        "breakdown",
        "unit",
        "country",
        "period",
        "import_config",
        "import_file",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("import_config")


admin.site.register(Fact, FactAdmin)


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)


class DataFileImportAdmin(admin.ModelAdmin):
    search_fields = ("description", "file")
    fields = (
        "file",
        "latest_import",
        "num_facts",
        "description",
        "user",
    )
    actions = ("trigger_import", "trigger_import_destructive")

    def get_readonly_fields(self, request, obj=None):
        # `errors` has a custom widget and is disabled at the form level
        if obj:  # edit
            return (
                "file",
                "latest_import",
                "user",
                "num_facts",
            )
        else:  # new object
            return (
                "latest_import",
                "user",
                "num_facts",
            )

    list_display = ("file_name", "latest_import", "num_facts", "created_at", "user")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_facts=Count("facts"))

    @admin.display(description="Facts Count", ordering="num_facts")
    def num_facts(self, obj):
        url = (
            reverse("admin:core_fact_changelist") + f"?import_file__pk__exact={obj.pk}"
        )
        return mark_safe(f"<a href='{url}'>{obj.num_facts}</a>")

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "user"):
            obj.user = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description="Trigger import for selected files")
    def trigger_import(self, request, queryset):
        return self._trigger_import(request, queryset)

    @admin.action(
        description="Delete existing facts and trigger import for selected files"
    )
    def trigger_import_destructive(self, request, queryset):
        return self._trigger_import(request, queryset, delete_existing=True)

    def _trigger_import(self, request, queryset, **kwargs):
        for obj in queryset:
            obj.queue_import(created_by=request.user, **kwargs)

        self.message_user(
            request,
            "Import tasks have been queued for the selected configurations",
            level=messages.SUCCESS,
        )

        return redirect("admin:core_datafileimporttask_changelist")

    @admin.display(description="Latest Task")
    def latest_import(self, obj):
        if not obj.latest_task:
            return
        url = reverse(
            "admin:core_datafileimporttask_change",
            kwargs={"object_id": obj.latest_task.id},
        )
        return mark_safe(f"<a href='{url}'>{obj.latest_task.status}</a>")


admin.site.register(DataFileImport, DataFileImportAdmin)


@admin.register(DataFileImportTask)
class DataFileImportTaskAdmin(TaskAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    search_fields = [
        "import_file__file",
        "import_file__description",
        "=id",
        "=job_id",
    ]
    list_filter = [
        ImportFileFilter,
        "created_on",
        "started_on",
        "status",
    ]
    autocomplete_fields = ("import_file",)

    list_display = [
        "__str__",
        "import_file_link",
        "delete_existing",
        "created_on_display",
        "created_by",
        "started_on_display",
        "completed_on_display",
        "duration_display",
        "status_display",
        "progress_display",
        "mode",
    ]

    @admin.display(description="Import File", ordering="import_file")
    def import_file_link(self, obj):
        url = reverse(
            "admin:core_datafileimport_change",
            kwargs={"object_id": obj.import_file.id},
        )
        return mark_safe(f"<a href='{url}'>{obj.import_file}</a>")
