from constance import config
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView

from digital_agenda.apps.core.views.facts import EUROSTAT_FLAGS


class AppSettingsView(APIView):
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(never_cache)
    def get(self, *args, **kwargs):
        return Response(
            {
                "analytics_server": config.MATOMO_SERVER,
                "analytics_site_id": config.MATOMO_SITE_ID,
                "global_banner_enabled": config.GLOBAL_BANNER_ENABLED,
                "eurostat_flags": EUROSTAT_FLAGS,
            },
        )
