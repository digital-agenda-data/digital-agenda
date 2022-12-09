import json

from django.contrib import admin
from django.db import models
from django import forms

from admin_auto_filters.filters import AutocompleteFilter
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
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
    field_name = "data_source"


@admin.register(Indicator)
class IndicatorAdmin(DimensionAdmin):
    list_filter = [DataSourceFilter]
    autocomplete_fields = (
        "breakdowns",
        "units",
        "periods",
        "countries",
    )


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


class FactAdmin(admin.ModelAdmin):
    list_display = (
        "indicator",
        "breakdown",
        "unit",
        "country",
        "period",
        "value",
        "flags",
    )
    list_filter = [IndicatorFilter]
    list_per_page = 50


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

    fields = (
        "file",
        "status",
        "description",
        "user",
        "errors",
    )

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
            )
        else:  # new object
            return (
                "status",
                "user",
            )

    list_display = ("file_name", "status", "created_at", "user")

    form = DataFileImportForm

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "user"):
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(DataFileImport, DataFileImportAdmin)
