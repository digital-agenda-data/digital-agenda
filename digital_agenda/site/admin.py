from constance import config
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class DigitalAgendaAdminSite(AdminSite):
    site_title = "Digital Agenda Data Administration"
    site_header = "Digital Agenda Data Administration"
    index_title = "Digital Agenda Data Administration"

    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        if config.PASSWORD_LOGIN_ENABLED:
            return super().login(request, extra_context=extra_context)

        if request.method == "GET" and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse("admin:index", current_app=self.name)
            return HttpResponseRedirect(index_path)

        if config.EU_LOGIN_ENABLED:
            cas_path = reverse("cas_ng_login", current_app=self.name)
            return HttpResponseRedirect(cas_path)

        raise Http404


class DigitalAgendaAdminConfig(AdminConfig):
    default_site = "digital_agenda.site.admin.DigitalAgendaAdminSite"
