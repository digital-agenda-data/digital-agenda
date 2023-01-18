import textwrap

from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget

from digital_agenda.apps.estat.models import *
from digital_agenda.apps.estat.tasks import import_from_config


@admin.register(GeoGroup)
class GeoGroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    list_display = ("code", "size", "note", "geo_codes")
    search_fields = ("code",)


DIMENSION_DESCRIPTION = """
Choose what dimension from the ESTAT dataset to take values from. Notes:
<dl>
    <li>Surrogate fields will be taken as hardcoded values instead.</li>
    <li>Non-existing values are automatically created on import.</li>
</dl>
"""
FILTERS_DESCRIPTION = """
All datapoints must pass ALL of the defined filters, there is no support for logical 
'OR' combinations between the filters. For such cases multiple similar configurations 
must be defined instead. Example filter:

<pre>
{
  "isced11": ["ED35", "ED5-8"],
  "iscedf13": ["F06"]
}
</pre>
"""
MAPPING_DESCRIPTION = """
Transform ESTAT codes before inserting into DB. Values not specified here are 
taken as they are instead. Example:

<pre>
{
  "country": {
    "EU28": "EU",
    "EU27_2020": "EU"
  }
}
</pre>
"""


@admin.register(ImportConfig)
class ImportConfigAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    list_display = (
        "code",
        "indicator",
        "breakdown",
        "country_group",
        "period_start",
        "period_end",
        "last_import_time",
        "num_facts",
        "title",
        "status_short",
    )
    search_fields = ("code", "title")
    readonly_fields = (
        "last_import_time",
        "num_facts",
        "status",
    )
    autocomplete_fields = ("country_group",)
    actions = ("trigger_import", "trigger_import_destructive")

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "code",
                    "title",
                    "last_import_time",
                    "status",
                    "num_facts",
                ]
            },
        ),
        (
            "Dimensions",
            {
                "description": DIMENSION_DESCRIPTION,
                "fields": [
                    ("indicator", "indicator_is_surrogate"),
                    ("breakdown", "breakdown_is_surrogate"),
                    ("country", "country_is_surrogate"),
                    ("period", "period_is_surrogate"),
                    ("unit", "unit_is_surrogate"),
                ],
            },
        ),
        (
            "Filters",
            {
                "description": FILTERS_DESCRIPTION,
                "fields": [
                    "country_group",
                    "period_start",
                    "period_end",
                    "filters",
                ],
            },
        ),
        (
            "Mappings",
            {
                "description": MAPPING_DESCRIPTION,
                "fields": ["mappings"],
            },
        ),
    )

    @admin.action(description="Trigger import for selected configs")
    def trigger_import(self, request, queryset):
        self._trigger_import(request, queryset)

    @admin.action(
        description="Delete existing facts and trigger import for selected configs"
    )
    def trigger_import_destructive(self, request, queryset):
        self._trigger_import(
            request, queryset, force_download=True, delete_existing=True
        )

    def _trigger_import(
        self, request, queryset, force_download=False, delete_existing=False
    ):
        queryset.update(status="Queued")
        for obj in queryset:
            import_from_config.delay(
                obj.id, force_download=force_download, delete_existing=delete_existing
            )

        self.message_user(
            request,
            "Import tasks have been queued for the selected configurations",
            level=messages.SUCCESS,
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_facts=Count("facts"))

    @admin.display(description="Facts Count", ordering="num_facts")
    def num_facts(self, obj):
        url = (
            reverse("admin:core_fact_changelist")
            + f"?import_config__pk__exact={obj.pk}"
        )
        return mark_safe(f"<a href='{url}'>{obj.num_facts}</a>")

    @admin.display(description="Status", ordering="status")
    def status_short(self, obj):
        return textwrap.shorten(obj.status, 50)
