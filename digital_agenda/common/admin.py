from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from django.db.models import Exists
from django.db.models import ManyToManyField
from django.db.models import OuterRef
from django.urls import reverse
from django.utils.safestring import mark_safe

from digital_agenda.apps.core.models import Fact


class HasChangesAdminMixin:
    """MixIn that add the 'has-changes' class to fieldsets that have any field with
    changed (i.e. not default) values.
    """

    def has_changes(self, fields, obj=None):
        if not obj:
            return False

        for field_group in fields:
            if not isinstance(field_group, (list, tuple)):
                field_group = (field_group,)

            for field_name in field_group:
                value = getattr(obj, field_name)
                field = getattr(self.model, field_name).field

                if isinstance(field, ManyToManyField):
                    if value.exists():
                        return True
                elif value != field.default:
                    return True

        return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        for name, options in fieldsets:
            if not options.get("classes"):
                options["classes"] = []

            if self.has_changes(options["fields"], obj=obj):
                options["classes"].append("has-changes")

        return fieldsets


class HasFactsFilter(SimpleListFilter):
    title = "Has Facts"

    parameter_name = "has_facts"

    def lookups(self, request, model_admin):
        return [("true", "Yes"), ("false", "No")]

    def queryset(self, request, queryset):
        val = self.value()
        if val == "true":
            return queryset.filter(has_facts=True)
        if val == "false":
            return queryset.filter(has_facts=False)

        return queryset


class HasFactsAdminMixIn:
    """Admin Mixin that adds:

    - A flag determining whether there are facts linked to the corresponding dimension
    - A list filter to either get all entries with zero facts or all entries with
      more than one fact

    Only works if the model has a direct relationship with the Fact model.
    """

    facts_filter: str = None

    def get_list_filter(self, request):
        result = super().get_list_filter(request)
        return [*result, HasFactsFilter]

    def get_readonly_fields(self, request, obj=None):
        result = super().get_readonly_fields(request, obj=obj)
        if "has_facts" not in result:
            return [*result, "has_facts"]
        return result

    def get_list_display(self, request):
        result = super().get_list_display(request)
        if "has_facts" not in result:
            return [*result, "has_facts"]
        return result

    def get_queryset(self, request):
        subquery = Fact.objects.filter((self.facts_filter, OuterRef("pk")))
        return super().get_queryset(request).annotate(has_facts=Exists(subquery))

    @admin.display(description="Has Facts", ordering="has_facts", boolean=True)
    def has_facts(self, obj):
        return obj.has_facts
