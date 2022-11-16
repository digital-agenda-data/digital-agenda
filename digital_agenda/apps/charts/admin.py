from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from digital_agenda.apps.charts.models import ChartGroup


class IndicatorGroupTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    extra = 0
    model = ChartGroup.indicator_groups.through
    autocomplete_fields = ("indicator_group",)


@admin.register(ChartGroup)
class ChartGroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ("code", "name", "short_name")
    list_display = (
        "code",
        "name",
        "short_name",
        "display_order",
    )
    autocomplete_fields = ("periods",)
    inlines = (IndicatorGroupTabularInline,)

