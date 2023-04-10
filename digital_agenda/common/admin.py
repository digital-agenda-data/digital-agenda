from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from django.db.models import ManyToManyField
from django.urls import reverse
from django.utils.safestring import mark_safe


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


class ZeroFactsFilter(SimpleListFilter):
    title = "Fact Count"

    parameter_name = "num_facts__is_zero"

    def lookups(self, request, model_admin):
        return [("true", "No facts"), ("false", "At least one fact")]

    def queryset(self, request, queryset):
        val = self.value()
        if val == "true":
            return queryset.filter(num_facts=0)
        if val == "false":
            return queryset.filter(num_facts__gt=0)

        return queryset


class NumFactsAdminMixIn:
    """Admin Mixin that adds:

    - an aggregated fact count for the dimension, as a link to the fact admin
      filtered by the corresponding dimension
    - a list filter to either get all entries with zero facts or all entries with
      more than one fact

    Only works if the model has a direct relationship with the Fact model.
    """

    facts_rel_name = "facts"
    num_facts_filter = None

    def get_list_filter(self, request):
        result = super().get_list_filter(request)
        return [*result, ZeroFactsFilter]

    def get_readonly_fields(self, request, obj=None):
        result = super().get_readonly_fields(request, obj=obj)
        if "num_facts" not in result:
            return [*result, "num_facts"]
        return result

    def get_list_display(self, request):
        result = super().get_list_display(request)
        if "num_facts" not in result:
            return [*result, "num_facts"]
        return result

    def get_queryset(self, request):
        return (
            super().get_queryset(request).annotate(num_facts=Count(self.facts_rel_name))
        )

    @admin.display(description="Facts Count", ordering="num_facts")
    def num_facts(self, obj):
        assert self.num_facts_filter, "'num_facts_filter' not set"
        url = (
            reverse("admin:core_fact_changelist") + f"?{self.num_facts_filter}={obj.pk}"
        )
        return mark_safe(f"<a href='{url}'>{obj.num_facts}</a>")
