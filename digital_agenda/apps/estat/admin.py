from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin, messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget
from django_task.admin import TaskAdmin

from digital_agenda.apps.estat.models import *


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
        "num_facts",
        "latest_import",
        "title",
    )
    search_fields = ("code", "title")
    readonly_fields = (
        "num_facts",
        "latest_import",
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
        return self._trigger_import(request, queryset)

    @admin.action(
        description="Delete existing facts and trigger import for selected configs"
    )
    def trigger_import_destructive(self, request, queryset):
        return self._trigger_import(
            request, queryset, force_download=True, delete_existing=True
        )

    def _trigger_import(self, request, queryset, **kwargs):
        for obj in queryset:
            obj.queue_import(created_by=request.user, **kwargs)

        self.message_user(
            request,
            "Import tasks have been queued for the selected configurations",
            level=messages.SUCCESS,
        )

        return redirect("admin:estat_importfromconfigtask_changelist")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_facts=Count("facts"))

    @admin.display(description="Facts Count", ordering="num_facts")
    def num_facts(self, obj):
        url = (
            reverse("admin:core_fact_changelist")
            + f"?import_config__pk__exact={obj.pk}"
        )
        return mark_safe(f"<a href='{url}'>{obj.num_facts}</a>")

    @admin.display(description="Latest Task")
    def latest_import(self, obj):
        if not obj.latest_task:
            return
        url = reverse(
            "admin:estat_importfromconfigtask_change",
            kwargs={"object_id": obj.latest_task.id},
        )
        return mark_safe(f"<a href='{url}'>{obj.latest_task.status}</a>")


class ImportConfigFilter(AutocompleteFilter):
    title = "Import Config"
    field_name = "import_config"


@admin.register(ImportFromConfigTask)
class ImportFromConfigTaskAdmin(TaskAdmin):
    search_fields = [
        "import_config__code",
        "import_config__title",
        "=id",
        "=job_id",
    ]
    list_filter = [
        ImportConfigFilter,
        "created_on",
        "started_on",
        "status",
    ]
    autocomplete_fields = ("import_config",)

    list_display = [
        "__str__",
        "import_config_link",
        "delete_existing",
        "force_download",
        "created_on_display",
        "created_by",
        "started_on_display",
        "completed_on_display",
        "duration_display",
        "status_display",
        "progress_display",
        "mode",
    ]

    @admin.display(description="Import Config", ordering="import_config")
    def import_config_link(self, obj):
        url = reverse(
            "admin:estat_importconfig_change",
            kwargs={"object_id": obj.import_config.id},
        )
        return mark_safe(f"<a href='{url}'>{obj.import_config}</a>")
