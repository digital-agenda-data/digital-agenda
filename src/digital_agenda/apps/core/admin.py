from django.contrib import admin

from admin_auto_filters.filters import AutocompleteFilter
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

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


admin.site.register(Indicator, DimensionAdmin)


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
