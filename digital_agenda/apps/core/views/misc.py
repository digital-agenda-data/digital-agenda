from constance import config
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from digital_agenda.apps.core.views.facts import EUROSTAT_FLAGS


class AppSettingsView(APIView):
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(never_cache)
    def get(self, *args, **kwargs):
        return Response(
            {
                "analytics_site_id": config.EUROPA_ANALYTICS_SITE_ID,
                "global_banner_enabled": config.GLOBAL_BANNER_ENABLED,
                "eurostat_flags": EUROSTAT_FLAGS,
                "sentry_dsn": settings.SENTRY_DSN,
                "environment_name": settings.ENVIRONMENT_NAME,
                "chart_credits": config.CHART_CREDITS,
            }
        )


class SetTimezoneView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = Response(status=HTTP_204_NO_CONTENT)
        response.set_cookie(
            settings.TIMEZONE_COOKIE,
            request.data["timezone"],
            secure=settings.HAS_HTTPS,
            samesite="strict",
        )
        return response
