from django.db.models import ManyToManyField


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
