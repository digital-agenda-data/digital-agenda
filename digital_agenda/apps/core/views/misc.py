from constance import config
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView


class AppSettingsView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, *args, **kwargs):
        return Response(
            {
                "analytics_server": config.MATOMO_SERVER,
                "analytics_site_id": config.MATOMO_SITE_ID,
            },
        )
