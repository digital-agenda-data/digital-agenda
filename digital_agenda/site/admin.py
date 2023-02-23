from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig


class DigitalAgendaAdminSite(AdminSite):
    site_title = "Digital Agenda Data Administration"
    site_header = "Digital Agenda Data Administration"
    index_title = "Digital Agenda Data Administration"


class DigitalAgendaAdminConfig(AdminConfig):
    default_site = "digital_agenda.site.admin.DigitalAgendaAdminSite"
