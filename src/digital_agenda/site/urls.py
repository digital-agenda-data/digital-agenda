from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


api_urlpatterns = [
    path("", include("digital_agenda.apps.core.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/", include((api_urlpatterns, "api"))),
    path("ht/", include("health_check.urls")),
    path("ws/ht/", include("health_check.urls", namespace="ws-ht")),
    path("dashboard/", include("django_sql_dashboard.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
