import django_cas_ng.views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from digital_agenda.apps.accounts import views as accounts_views
from digital_agenda.apps.shortner.views import ChartRedirectView

from django.contrib.admin import site
import adminactions.actions as actions

# register all adminactions
actions.add_to_site(site)

api_urlpatterns = [
    path("", include("digital_agenda.apps.core.urls")),
    path("", include("digital_agenda.apps.charts.urls")),
    path("", include("digital_agenda.apps.shortner.urls")),
]

urlpatterns = [
    path("s/<id>/", ChartRedirectView.as_view(), name="chart_redirect"),
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
    path("django-rq/", include("django_rq.urls")),
    path("django_task/", include("django_task.urls", namespace="django_task")),
    path("admin/adminactions/", include("adminactions.urls")),
    path(
        "admin/cas/login", django_cas_ng.views.LoginView.as_view(), name="cas_ng_login"
    ),
    path(
        "admin/cas/logout",
        django_cas_ng.views.LogoutView.as_view(),
        name="cas_ng_logout",
    ),
    path(
        "admin/password_reset/",
        accounts_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "admin/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "admin/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("admin/", admin.site.urls),
    path(
        "admin/ckeditor5/",
        include("django_ckeditor_5.urls"),
        name="ck_editor_5_upload_file",
    ),
    path("", RedirectView.as_view(pattern_name="admin:index")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.DJANGO_DEBUG_TOOLBAR:
        try:
            import debug_toolbar
        except ImportError:
            pass
        else:
            urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
