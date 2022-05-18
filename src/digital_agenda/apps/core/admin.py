from django.contrib import admin
from django.db.models.functions import Lower

from admin_auto_filters.filters import AutocompleteFilter

from .models import (
    DataSource,
    DataSourceReference,
    IndicatorGroup,
    Indicator,
    BreakdownGroup,
    Breakdown,
    Unit,
    Country,
    Period,
    Fact,
)


class DataSourceReferenceInline(admin.TabularInline):
    model = DataSourceReference
    verbose_name = "References"


class DataSourceAdmin(admin.ModelAdmin):
    inlines = [DataSourceReferenceInline]


admin.site.register(DataSource, DataSourceAdmin)


class DimensionAdmin(admin.ModelAdmin):
    list_display = ("code", "label")
    search_fields = ("code", "label")
    list_per_page = 20

    def get_ordering(self, request):
        return [Lower("code")]


admin.site.register(IndicatorGroup, DimensionAdmin)
admin.site.register(Indicator, DimensionAdmin)
admin.site.register(BreakdownGroup, DimensionAdmin)
admin.site.register(Breakdown, DimensionAdmin)
admin.site.register(Unit, DimensionAdmin)
admin.site.register(Country, DimensionAdmin)
admin.site.register(Period, DimensionAdmin)


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
