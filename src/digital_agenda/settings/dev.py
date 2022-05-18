import logging

from .base import *
from django.conf import (
    settings as computed_settings,
)  # DEBUG is forced to False during tests


DJANGO_DEBUG_TOOLBAR = get_bool_env_var("DJANGO_DEBUG_TOOLBAR", "yes")

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS += ["django_extensions", "drf_spectacular"]
if DJANGO_DEBUG_TOOLBAR:
    INSTALLED_APPS += ["debug_toolbar"]


if DEBUG and DJANGO_DEBUG_TOOLBAR:
    import socket

    def show_toolbar(request):
        return computed_settings.DEBUG and (
            request.META.get("REMOTE_ADDR") in INTERNAL_IPS
            or request.META.get("HTTP_X_REAL_IP") in INTERNAL_IPS
        )

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
    MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": f"{__name__}.show_toolbar",
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 4,
        },
    },
]

if DEBUG:
    MIDDLEWARE.append("request_logging.middleware.LoggingMiddleware")

REQUEST_LOGGING_DATA_LOG_LEVEL = logging.INFO
REQUEST_LOGGING_MAX_BODY_LENGTH = 1000
