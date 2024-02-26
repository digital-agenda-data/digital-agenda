from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from constance.admin import ConstanceAdmin, Config
from constance.forms import ConstanceForm
from django.core.exceptions import ValidationError

from .forms import UserCreationForm, UserChangeForm
from .models import User

# We are not using authentication groups. If we want to ever add this back, we need
# to implement permission checks for all the custom actions we have in the admin.
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm
    search_fields = ("email",)
    ordering = ("email",)
    list_display = ("email", "is_active", "is_superuser", "last_login")
    list_filter = ("is_active", "is_superuser")
    readonly_fields = ("last_login", "created_at", "updated_at")
    fieldsets = (
        (
            None,
            {"fields": ("email",)},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                )
            },
        ),
        (
            "Meta",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_superuser",
                ),
            },
        ),
    )


class CustomConfigForm(ConstanceForm):
    def clean(self):
        data = super().clean()
        if not any([data["PASSWORD_LOGIN_ENABLED"], data["EU_LOGIN_ENABLED"]]):
            raise ValidationError(
                {
                    "PASSWORD_LOGIN_ENABLED": (
                        "At least one alternative login method must be enabled to "
                        "disable password login."
                    )
                }
            )
        return data


class ConfigAdmin(ConstanceAdmin):
    change_list_form = CustomConfigForm


admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)
