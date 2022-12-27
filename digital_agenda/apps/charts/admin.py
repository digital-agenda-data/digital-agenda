from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db.models import ManyToManyField

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
        "display_order",
        "code",
        "chart_group",
        "name",
        "chart_type",
        "is_draft",
    )
    exclude = ("display_order",)
    autocomplete_fields = (
        "chart_group",
        *Chart.m2m_filter_options,
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        result = super().formfield_for_manytomany(db_field, request, **kwargs)
        result.widget.attrs["style"] = "width: 580px;"
        return result

    def has_changes(self, private_field, obj=None):
        if not obj:
            return False

        for subfield in private_field.subfields.values():
            value = getattr(obj, subfield.name)
            if isinstance(subfield, ManyToManyField):
                if value.exists():
                    return True
            elif value != subfield.default:
                return True

        return False

    def get_fieldsets(self, request, obj=None):
        result = [
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
            )
        ]
        for private_field in Chart._meta.private_fields:
            classes = ["wide", "collapse"]
            if self.has_changes(private_field, obj=obj):
                classes.append("has-changes")

            subfields = [subfield.name for subfield in private_field.subfields.values()]
            result.append(
                (
                    private_field.verbose_name.title(),
                    {
                        "classes": classes,
                        "fields": subfields,
                    },
                )
            )

        return result


@admin.register(ChartGroup)
class ChartGroupAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ("code", "name", "short_name", "description")
    list_display = (
        "display_order",
        "code",
        "name",
        "short_name",
        "is_draft",
    )
    filter_horizontal = ("periods", "indicator_groups")
