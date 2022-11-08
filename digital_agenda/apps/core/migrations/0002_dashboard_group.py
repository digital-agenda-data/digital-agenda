from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.management import create_permissions


dashboard_permissions = (
    "add_dashboard",
    "change_dashboard",
    "delete_dashboard",
    "view_dashboard",
    "execute_sql",
    "add_dashboardquery",
    "change_dashboardquery",
    "delete_dashboardquery",
    "view_dashboardquery",
)


def add_dashboard_group(apps, schema_editor):

    # Make sure permissions exist
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    role, _ = Group.objects.get_or_create(name="Dashboard")
    for p in dashboard_permissions:
        perm = Permission.objects.get(codename=p)
        role.permissions.add(perm)
    role.save()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "__latest__"),
        ("django_sql_dashboard", "__latest__"),
        ("core", "0001_citext"),
    ]

    operations = [migrations.RunPython(add_dashboard_group)]
