from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin, messages
from django.contrib.admin import EmptyFieldListFilter
from django.db.models import Count
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget
from django_task.admin import TaskAdmin

from digital_agenda.apps.estat.models import *


@admin.register(ImportConfigTag)
class ImportConfigTagAdmin(admin.ModelAdmin):
    list_display = ("code",)
    search_fields = ("code",)
    ordering = ("code",)


@admin.register(GeoGroup)
class GeoGroupAdmin(admin.ModelAdmin):
    formfield_overrides = {models.JSONField: {"widget": JSONEditorWidget}}
    list_display = ("code", "size", "note", "geo_codes")
    search_fields = ("code",)
    ordering = ("code",)


DIMENSION_DESCRIPTION = """
Choose what dimension from the ESTAT dataset to take values from. Notes:
<dl>
    <li>Surrogate fields will be taken as hardcoded values instead.</li>
    <li>Non-existing values are automatically created on import.</li>
    <li>Imported values can be transformed my using the mapping fields below.</li>
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
    save_as = True
    list_per_page = 20
    formfield_overrides = {models.JSONField: {"widget": JSONEditorWidget}}
    list_display = (
        "code",
        "country_group",
        "period_start",
        "period_end",
        "num_facts",
        "latest_run_date",
        "latest_import",
        "title",
        "tag_codes",
        "has_additional_remarks",
        "new_version_available",
    )
    search_fields = ("code", "title", "indicator", "tags__code", "filters", "mappings")
    list_filter = (
        "tags",
        ("additional_remarks", EmptyFieldListFilter),
        "new_version_available",
        "disable_check_updates",
    )
    readonly_fields = (
        "num_facts",
        "latest_import",
        "latest_run_date",
        "data_last_update",
        "datastructure_last_update",
        "datastructure_last_version",
        "new_version_available",
        "databrowser_link",
    )
    autocomplete_fields = ("country_group", "tags")
    actions = ("trigger_import", "trigger_import_destructive")

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "code",
                    "title",
                    "tags",
                    "additional_remarks",
                    "conflict_resolution",
                    "disable_check_updates",
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
                    ("reference_period", "reference_period_is_surrogate"),
                    ("remarks", "remarks_is_surrogate"),
                ],
            },
        ),
        (
            "Filters",
            {
                "description": FILTERS_DESCRIPTION,
                "fields": ["country_group", "period_start", "period_end", "filters"],
            },
        ),
        ("Mappings", {"description": MAPPING_DESCRIPTION, "fields": ["mappings"]}),
        (
            "Metadata",
            {
                "fields": [
                    "num_facts",
                    "latest_import",
                    "latest_run_date",
                    "data_last_update",
                    "datastructure_last_update",
                    "datastructure_last_version",
                    "databrowser_link",
                    "new_version_available",
                ]
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
        obj = None
        for obj in queryset:
            obj.queue_import(created_by=request.user, **kwargs)

        self.message_user(
            request,
            "Import tasks have been queued for the selected configurations",
            level=messages.SUCCESS,
        )

        url = reverse("admin:estat_importfromconfigtask_changelist")
        if obj and queryset.count() == 1:
            url += f"?import_config={obj.id}"
        return redirect(url)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                num_facts=Count("facts"),
                latest_run_date=Subquery(
                    ImportFromConfigTask.objects.filter(import_config_id=OuterRef("id"))
                    .order_by("-created_on")
                    .values("created_on")[:1]
                ),
            )
            .prefetch_related(
                "tags",
                "country_group",
                Prefetch(
                    "tasks",
                    ImportFromConfigTask.objects.all().order_by("-created_on"),
                    to_attr="prefetched_latest_tasks",
                ),
            )
        )

    @admin.display(description="Facts Count", ordering="num_facts")
    def num_facts(self, obj):
        url = reverse("admin:core_fact_changelist") + f"?import_config={obj.pk}"
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

    @admin.display(description="Latest Run", ordering="latest_run_date")
    def latest_run_date(self, obj):
        return obj.latest_run_date

    @admin.display(description="Tags")
    def tag_codes(self, obj):
        return ", ".join(tag.code for tag in obj.tags.all())

    @admin.display(description="Databrowser")
    def databrowser_link(self, obj):
        if not obj.code:
            return "-"
        url = f"https://ec.europa.eu/eurostat/databrowser/view/{obj.code}/default/table?lang=en"
        return mark_safe(f'<a href="{url}" target="_blank">{url}</a>')

    @admin.display(description="Has Remarks", boolean=True)
    def has_additional_remarks(self, obj):
        return bool(obj.additional_remarks)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


@admin.register(ImportFromConfigTask)
class ImportFromConfigTaskAdmin(TaskAdmin):
    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget(options={"mode": "view", "modes": ["view"]})
        }
    }

    search_fields = ["import_config__code", "import_config__title", "=id", "=job_id"]
    list_filter = [
        AutocompleteFilterFactory("import config", "import_config"),
        "created_on",
        "started_on",
        "status",
    ]
    autocomplete_fields = ("import_config",)
    ordering = ("-created_on",)

    list_display = [
        "__str__",
        "import_config_link",
        "delete_existing",
        "force_download",
        "created_on",
        "duration_display",
        "status_display",
    ]

    @admin.display(description="Import Config", ordering="import_config")
    def import_config_link(self, obj):
        url = reverse(
            "admin:estat_importconfig_change",
            kwargs={"object_id": obj.import_config.id},
        )
        return mark_safe(f"<a href='{url}'>{obj.import_config}</a>")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        try:
            fields.remove("errors")
        except ValueError:
            pass
        return fields

    def get_exclude(self, request, obj=None):
        if not obj:
            return ["errors"]

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        fields.remove("log_link_display")
        return fields
