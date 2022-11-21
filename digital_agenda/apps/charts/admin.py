from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.charts.models import ChartGroup


@admin.register(Chart)
class ChartAdmin(SortableAdminMixin, admin.ModelAdmin):
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
        "code",
        "chart_type",
        "is_draft",
        "name",
        "chart_group",
        "display_order",
    )
    exclude = ("display_order",)
    autocomplete_fields = ("chart_group",)


class ChartInlineAdmin(SortableInlineAdminMixin, admin.StackedInline):
    prepopulated_fields = {**ChartAdmin.prepopulated_fields}
    model = Chart
    extra = 0


@admin.register(ChartGroup)
class ChartGroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ("code", "name", "short_name", "description")
    list_display = (
        "code",
        "is_draft",
        "name",
        "short_name",
        "display_order",
    )
    filter_horizontal = ("periods", "indicator_groups")
    inlines = (ChartInlineAdmin,)
