from constance import config
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from digital_agenda.apps.core.models import StaticPage
from digital_agenda.apps.core.serializers import StaticPageSerializer
from digital_agenda.apps.core.views.facts import EUROSTAT_FLAGS


class AppSettingsView(APIView):
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(never_cache)
    def get(self, *args, **kwargs):
        return Response(
            {
                "analytics_site_id": config.EUROPA_ANALYTICS_SITE_ID,
                "global_banner_enabled": config.GLOBAL_BANNER_ENABLED,
                "cck_enabled": config.CCK_ENABLED,
                "eurostat_flags": EUROSTAT_FLAGS,
                "sentry_dsn": settings.SENTRY_DSN,
                "environment_name": settings.ENVIRONMENT_NAME,
                "chart_credits": config.CHART_CREDITS,
                "captcha_enabled": settings.CAPTCHA_ENABLED,
            }
        )


class StaticPageViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "code"
    serializer_class = StaticPageSerializer
    queryset = StaticPage.objects.all()
