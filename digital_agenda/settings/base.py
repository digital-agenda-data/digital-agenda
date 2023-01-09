import logging
import os
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

env = environ.Env()

if os.path.exists(str(BASE_DIR / ".env")):
    env.read_env(str(BASE_DIR / ".env"))

HAS_HTTPS = env.bool("HAS_HTTPS", default=False)
PROTOCOL = "https://" if HAS_HTTPS else "http://"

BACKEND_HOST = env.list("BACKEND_HOST")
FRONTEND_HOST = env.list("FRONTEND_HOST")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_CACHE_DB = 0
REDIS_CELERY_DB = 1

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG
DEBUG = env.bool("DEBUG", default=False)

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY
SECRET_KEY = env.str("SECRET_KEY")

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-CSRF_COOKIE_SECURE
CSRF_COOKIE_SECURE = HAS_HTTPS

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECURE_SSL_REDIRECT
SECURE_SSL_REDIRECT = HAS_HTTPS

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SESSION_COOKIE_SECURE
SESSION_COOKIE_SECURE = HAS_HTTPS

# https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [_host.rsplit(":", 1)[0] for _host in BACKEND_HOST]

# Application definition

DJANGO_APPS = [
    "django_admin_env_notice",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "digital_agenda.apps.accounts.apps.Config",
    "digital_agenda.apps.core.apps.Config",
    "digital_agenda.apps.estat.apps.Config",
    "digital_agenda.apps.charts.apps.Config",
]

THIRD_PARTY_APPS = [
    "adminsortable2",
    "ckeditor",
    "colorfield",
    "corsheaders",
    "django_filters",
    "admin_auto_filters",
    "psqlextra",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django_sql_dashboard",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "drf_spectacular",
    "django_json_widget",
    "django_extensions",
]

INSTALLED_APPS = LOCAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["content-disposition"]
CORS_ALLOWED_ORIGINS = [PROTOCOL + _host for _host in FRONTEND_HOST]

CSRF_TRUSTED_ORIGINS = [PROTOCOL + _host for _host in (FRONTEND_HOST + BACKEND_HOST)]


ROOT_URLCONF = "digital_agenda.site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Django doesn't expect the apps to be packaged one at this level
            # So we need to manually specify the path(s).
            BASE_DIR
            / "digital_agenda"
            / "apps"
            / "charts"
            / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_admin_env_notice.context_processors.from_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "digital_agenda.site.wsgi.application"
ASGI_APPLICATION = "digital_agenda.site.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_DASHBOARD_USER = env.str("POSTGRES_DASHBOARD_USER")
POSTGRES_DASHBOARD_PASSWORD = env.str("POSTGRES_DASHBOARD_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": POSTGRES_DB,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "OPTIONS": {"sslmode": "disable"},
        "CONN_MAX_AGE": None,
        "CONN_HEALTH_CHECKS": True,
    },
    "dashboard": {
        "ENGINE": "psqlextra.backend",
        "NAME": POSTGRES_DB,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
        "USER": POSTGRES_DASHBOARD_USER,
        "PASSWORD": POSTGRES_DASHBOARD_PASSWORD,
        "OPTIONS": {
            "options": "-c default_transaction_read_only=on -c statement_timeout=5000"
        },
        "CONN_MAX_AGE": None,
        "CONN_HEALTH_CHECKS": True,
    },
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}/{REDIS_CACHE_DB}",
        "OPTIONS": {
            "SOCKET_TIMEOUT": 5,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "digital_agenda",
        # Cache never expires by default
        "TIMEOUT": env.int("CACHE_TIMEOUT", default=None),
    }
}


AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/admin/login"


REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "EXCEPTION_HANDLER": "digital_agenda.common.exceptions.core_exception_handler",
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Digital Agenda Data Visualization Tool API",
    "VERSION": "",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = env.path("STATIC_ROOT")

# Media files / user uploads
# https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
MEDIA_URL = "/media/"
MEDIA_ROOT = env.path("MEDIA_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery
CELERY_BROKER_URL = f"redis://{REDIS_HOST}/{REDIS_CELERY_DB}"


BULK_DOWNLOAD_ROOT_URL = env.str(
    "BULK_DOWNLOAD_ROOT_URL",
    default="https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing",
)
BULK_DOWNLOAD_TIMEOUT = env.float("BULK_DOWNLOAD_TIMEOUT", default=5.0)
BULK_DOWNLOAD_DIR = env.path("BULK_DOWNLOAD_DIR")

DEFAULT_STORAGE_CLASS = "django.core.files.storage.FileSystemStorage"

IMPORT_FILES_SUBDIR = env.str("IMPORT_FILES_SUBDIR", default="import_files")
IMPORT_FILES_ALLOWED_EXTENSIONS = env.list(
    "IMPORT_FILES_ALLOWED_EXTENSIONS",
    default=["xls", "xlsx"],
)
IMPORT_FILES_ALLOWED_MIME_TYPES = env.list(
    "IMPORT_FILES_ALLOWED_MIME_TYPES",
    default=[
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "main_formatter": {
            "format": "%(levelname)s %(name)s: %(message)s "
            "(%(asctime)s; %(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "main_formatter",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "digital_agenda": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG" if env.bool("LOG_REQUESTS", default=False) else "ERROR",
            "propagate": False,
        },
        "django": {"handlers": ["console"]},
        "py.warnings": {"handlers": ["null"]},
        "asyncio": {"handlers": ["console"], "level": "WARNING"},
        "": {
            "handlers": ["console"],
            "level": "INFO" if DEBUG else "WARNING",
            "propagate": False,
        },
    },
}


if DEBUG:
    DJANGO_DEBUG_TOOLBAR = env.bool("DJANGO_DEBUG_TOOLBAR", default=True)

    INTERNAL_IPS = ["127.0.0.1"]

    if DJANGO_DEBUG_TOOLBAR:
        INSTALLED_APPS += ["debug_toolbar"]

    if DEBUG and DJANGO_DEBUG_TOOLBAR:
        import socket

        def show_toolbar(request):
            return DEBUG and (
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
