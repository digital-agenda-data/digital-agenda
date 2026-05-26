from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from digital_agenda.apps.shortner.models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(ImportExportModelAdmin):
    list_display = ("id", "chart", "query_arguments", "created_at")
