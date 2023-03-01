import json

from django.contrib import admin, messages
from django.db import models
from django import forms

from admin_auto_filters.filters import AutocompleteFilter
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget

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
)
from .tasks import import_data_file


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


class DataFileImportForm(forms.ModelForm):
    """Disables the `errors` field"""

    class Meta:
        model = DataFileImport
        fields = ("errors",)
        widgets = {
            "errors": JSONEditorWidget(options={"mode": "view", "modes": ["view"]}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get("errors").disabled = True


class DataFileImportAdmin(admin.ModelAdmin):
    search_fields = ("description", "file")
    fields = (
        "file",
        "status",
        "num_facts",
        "description",
        "user",
        "errors",
    )
    actions = ("trigger_import", "trigger_import_destructive")

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    def get_readonly_fields(self, request, obj=None):
        # `errors` has a custom widget and is disabled at the form level
        if obj:  # edit
            return (
                "file",
                "status",
                "user",
                "num_facts",
            )
        else:  # new object
            return (
                "status",
                "user",
                "num_facts",
            )

    list_display = ("file_name", "status", "num_facts", "created_at", "user")

    form = DataFileImportForm

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
        self._trigger_import(request, queryset)

    @admin.action(
        description="Delete existing facts and trigger import for selected files"
    )
    def trigger_import_destructive(self, request, queryset):
        self._trigger_import(
            request, queryset, delete_existing=True
        )

    def _trigger_import(
        self, request, queryset, delete_existing=False
    ):
        queryset.update(status="Queued")
        for obj in queryset:
            import_data_file.delay(
                obj.id, delete_existing=delete_existing
            )

        self.message_user(
            request,
            "Import tasks have been queued for the selected files",
            level=messages.SUCCESS,
        )


admin.site.register(DataFileImport, DataFileImportAdmin)
