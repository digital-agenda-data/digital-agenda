import json

from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin, messages
from django.db import models
from django import forms

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


@admin.register(DataSource)
class DataSourceAdmin(DimensionAdmin):
    list_display = ("code", "label", "indicator_codes")

    @admin.display(description="Indicators")
    def indicator_codes(self, obj):
        return ", ".join(indicator.code for indicator in obj.indicators.all())

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("indicators")


class SortableDimensionAdmin(SortableAdminMixin, DimensionAdmin):
    pass


class IndicatorTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    model = IndicatorGroup.indicators.through
    autocomplete_fields = ("indicator",)


@admin.register(IndicatorGroup)
class IndicatorGroupAdmin(SortableDimensionAdmin):
    inlines = (IndicatorTabularInline,)
    list_filter = ["chartgroup", AutocompleteFilterFactory("indicator", "indicators")]


class DataSourceInline(admin.TabularInline):
    model = Indicator.data_sources.through
    autocomplete_fields = ("data_source",)
    extra = 0


@admin.register(Indicator)
class IndicatorAdmin(DimensionAdmin):
    list_filter = [AutocompleteFilterFactory("data source", "data_sources")]
    inlines = (DataSourceInline,)


class BreakdownTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    model = BreakdownGroup.breakdowns.through
    autocomplete_fields = ("breakdown",)


@admin.register(BreakdownGroup)
class BreakdownGroupAdmin(SortableDimensionAdmin):
    inlines = (BreakdownTabularInline,)
    list_filter = [AutocompleteFilterFactory("breakdown", "breakdowns")]


admin.site.register(Breakdown, DimensionAdmin)

admin.site.register(Unit, DimensionAdmin)

admin.site.register(Period, DimensionAdmin)


@admin.register(Country)
class CountryAdmin(DimensionAdmin):
    list_display = ("code", "is_group", "label", "alt_label", "color")
    list_filter = ("is_group",)


@admin.register(Fact)
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
        "indicator__groups__chartgroup",
        AutocompleteFilterFactory("import config", "import_config"),
        AutocompleteFilterFactory("import file", "import_file"),
        "indicator__data_sources",
        "indicator__groups",
        AutocompleteFilterFactory("indicator", "indicator"),
        "breakdown__groups",
        AutocompleteFilterFactory("breakdown", "breakdown"),
        AutocompleteFilterFactory("country", "country"),
        AutocompleteFilterFactory("period", "period"),
        AutocompleteFilterFactory("unit", "unit"),
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


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)


class DataFileImportAdmin(admin.ModelAdmin):
    search_fields = ("description", "file")
    fields = ("file", "latest_import", "num_facts", "description", "user")
    actions = ("trigger_import", "trigger_import_destructive")
    readonly_fields = ("latest_import", "user", "num_facts")

    list_display = ("file_name", "latest_import", "num_facts", "created_at", "user")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_facts=Count("facts"))

    @admin.display(description="Facts Count", ordering="num_facts")
    def num_facts(self, obj):
        url = reverse("admin:core_fact_changelist") + f"?import_file={obj.pk}"
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
            "Import tasks have been queued for the selected files",
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

    def response_post_save_add(self, request, obj):
        return redirect("admin:core_datafileimporttask_changelist")


admin.site.register(DataFileImport, DataFileImportAdmin)


class DataFileImportTaskForm(forms.ModelForm):
    """Disables the `errors` field"""

    class Meta:
        model = DataFileImportTask
        fields = ("errors",)
        widgets = {
            "errors": JSONEditorWidget(options={"mode": "view", "modes": ["view"]})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get("errors").disabled = True


@admin.register(DataFileImportTask)
class DataFileImportTaskAdmin(TaskAdmin):
    form = DataFileImportTaskForm
    formfield_overrides = {models.JSONField: {"widget": JSONEditorWidget}}

    search_fields = ["import_file__file", "import_file__description", "=id", "=job_id"]
    list_filter = [
        AutocompleteFilterFactory("import file", "import_file"),
        "created_on",
        "started_on",
        "status",
    ]
    autocomplete_fields = ("import_file",)
    ordering = ("-created_on",)

    list_display = [
        "__str__",
        "import_file_link",
        "delete_existing",
        "created_on",
        "duration_display",
        "status_display",
    ]

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        try:
            fields.remove("errors")
        except ValueError:
            pass
        return fields

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        fields.remove("log_link_display")
        return fields

    def has_add_permission(self, request):
        return False

    @admin.display(description="Import File", ordering="import_file")
    def import_file_link(self, obj):
        url = reverse(
            "admin:core_datafileimport_change", kwargs={"object_id": obj.import_file.id}
        )
        return mark_safe(f"<a href='{url}'>{obj.import_file}</a>")
