from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_urlpatterns = [
    path("", include("digital_agenda.apps.core.urls")),
    path("", include("digital_agenda.apps.charts.urls")),
    path("auth/", include("dj_rest_auth.urls")),
]

urlpatterns = [
    path("api/v1/", include((api_urlpatterns, "api"), namespace="v1")),
    path("api/v1/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("ht/", include("health_check.urls")),
    path("dashboard/", include("django_sql_dashboard.urls")),
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="admin:index")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
