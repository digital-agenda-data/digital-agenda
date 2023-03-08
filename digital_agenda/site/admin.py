from constance import config
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig


class DigitalAgendaAdminSite(AdminSite):
    site_title = "Digital Agenda Data Administration"
    site_header = "Digital Agenda Data Administration"
    index_title = "Digital Agenda Data Administration"

    def each_context(self, request):
        context = super().each_context(request)
        context["EU_LOGIN_ENABLED"] = config.EU_LOGIN_ENABLED
        context["GLOBAL_BANNER_ENABLED"] = config.GLOBAL_BANNER_ENABLED
        return context


class DigitalAgendaAdminConfig(AdminConfig):
    default_site = "digital_agenda.site.admin.DigitalAgendaAdminSite"
