import os
import socket
import logging
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

env = environ.Env()

if os.path.exists(str(BASE_DIR / ".env")):
    env.read_env(str(BASE_DIR / ".env"))

# Min year for various period settings in the app
MIN_YEAR = 1990

HAS_HTTPS = env.bool("HAS_HTTPS", default=False)
PROTOCOL = "https://" if HAS_HTTPS else "http://"

BACKEND_HOST = env.list("BACKEND_HOST")
FRONTEND_HOST = env.list("FRONTEND_HOST")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_CACHE_DB = 0
REDIS_TASK_DB = 1

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG
DEBUG = env.bool("DEBUG", default=False)

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY
SECRET_KEY = env.str("SECRET_KEY")

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-CSRF_COOKIE_SECURE
CSRF_COOKIE_SECURE = HAS_HTTPS

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECURE_SSL_REDIRECT
SECURE_SSL_REDIRECT = HAS_HTTPS

# https://docs.djangoproject.com/en/4.1/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SESSION_COOKIE_SECURE
SESSION_COOKIE_SECURE = HAS_HTTPS

# https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [_host.rsplit(":", 1)[0] for _host in BACKEND_HOST]

# Application definition

DJANGO_APPS = [
    "django_admin_env_notice",
    # "django.contrib.admin",
    "digital_agenda.site.admin.DigitalAgendaAdminConfig",
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
    "digital_agenda.apps.shortner.apps.Config",
]

THIRD_PARTY_APPS = [
    "django_rq",
    "django_task",
    "adminsortable2",
    "ckeditor",
    "colorfield",
    "corsheaders",
    "django_filters",
    "admin_auto_filters",
    "rest_framework",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "drf_spectacular",
    "django_json_widget",
    "django_extensions",
    "constance",
    "constance.backends.database",
    "django_cas_ng",
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
    "digital_agenda.apps.core.middleware.TimezoneMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "django_cas_ng.backends.CASBackend",
)


# https://djangocas.dev/docs/latest/configuration.html#
CAS_SERVER_URL = "https://ecas.ec.europa.eu/cas/"
CAS_VERSION = "3"
CAS_USERNAME_ATTRIBUTE = "email"
CAS_CREATE_USER = False

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["content-disposition"]
CORS_ALLOWED_ORIGINS = [PROTOCOL + _host for _host in FRONTEND_HOST]

CSRF_TRUSTED_ORIGINS = [PROTOCOL + _host for _host in (FRONTEND_HOST + BACKEND_HOST)]


ROOT_URLCONF = "digital_agenda.site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_admin_env_notice.context_processors.from_settings",
            ]
        },
    }
]

WSGI_APPLICATION = "digital_agenda.site.wsgi.application"
ASGI_APPLICATION = "digital_agenda.site.asgi.application"

# HashID
# https://github.com/nshafer/django-hashid-field

HASHID_FIELD_SALT = env.str("HASHID_FIELD_SALT")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "OPTIONS": {"sslmode": "disable"},
        "CONN_MAX_AGE": None,
        "CONN_HEALTH_CHECKS": True,
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}",
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

# EMAIL
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-backend
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-host
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-port
EMAIL_PORT = env.str("EMAIL_PORT", default="25")
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-host-user
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-email-use-tls
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-timeout
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=30)
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-DEFAULT_FROM_EMAIL
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="") or (
    "noreply@" + socket.gethostname()
)


AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
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
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_csv.renderers.CSVRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Digital Agenda Data Visualization Tool API",
    "VERSION": "",
    "SORT_OPERATION_PARAMETERS": False,
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_L10N = False

TIMEZONE_COOKIE = "X-Django-Timezone"

# See https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date
DATETIME_FORMAT = "d N Y, H:i O"
SHORT_DATETIME_FORMAT = "d-m-Y, H:i"
DATE_FORMAT = "d N Y"
SHORT_DATE_FORMAT = "d-m-Y"
TIME_FORMAT = "H:i:s"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

FS_DIR = BASE_DIR / ".fs"

STATIC_URL = "static/"
STATIC_ROOT = FS_DIR / "static"

# Media files / user uploads
# https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
MEDIA_URL = "/media/"
MEDIA_ROOT = FS_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Constance
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "FEEDBACK_EMAIL": (
        "feedback@example.com",
        "Email addresses where feedback messages are sent to; multiple addresses can be specified separated by comma",
    ),
    "GLOBAL_BANNER_ENABLED": (True, "Enable the Global banner component (Globan)"),
    "EU_LOGIN_ENABLED": (True, "Enable login with EU login CAS Server"),
    "MATOMO_SERVER": (
        "https://digital-agenda-data.eu/analytics/",
        "Matomo server; analytics are disabled if this is not set",
    ),
    "MATOMO_SITE_ID": ("", "Matomo Site ID; analytics are disabled if this is not set"),
    "ESTAT_UPDATE_ALERT_EMAILS": (
        "",
        "Alerts are automatically sent to all staff whenever datasets are updated in ESTAT. This setting can be used "
        "to specify a list of addresses separated by comma that should receive the alerts instead.",
    ),
}
CONSTANCE_CONFIG_FIELDSETS = (
    ("Feedback", {"collapse": False, "fields": ("FEEDBACK_EMAIL",)}),
    (
        "European Commission WebTools",
        {"collapse": False, "fields": ("GLOBAL_BANNER_ENABLED", "EU_LOGIN_ENABLED")},
    ),
    ("Analytics", {"collapse": False, "fields": ("MATOMO_SERVER", "MATOMO_SITE_ID")}),
    ("Alerts", {"collapse": False, "fields": ("ESTAT_UPDATE_ALERT_EMAILS",)}),
)


# Task Queue (RQ)

RQ = {"DEFAULT_RESULT_TTL": 0}


RQ_QUEUES = {"default": {"HOST": REDIS_HOST, "PORT": REDIS_PORT, "DB": REDIS_TASK_DB}}

# Hide RQ admin, since we are using Django Task models instead
RQ_SHOW_ADMIN_LINK = False

ESTAT_DOWNLOAD_BASE_URL = env.str(
    "ESTAT_DOWNLOAD_BASE_URL",
    default="https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/",
).strip("/")
ESTAT_DOWNLOAD_TIMEOUT = env.float("ESTAT_DOWNLOAD_TIMEOUT", default=30.0)
ESTAT_DOWNLOAD_DIR = FS_DIR / "estat"
ESTAT_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


IMPORT_FILES_SUBDIR = env.str("IMPORT_FILES_SUBDIR", default="import_files")
IMPORT_FILES_ALLOWED_EXTENSIONS = env.list(
    "IMPORT_FILES_ALLOWED_EXTENSIONS", default=["xls", "xlsx"]
)
IMPORT_FILES_ALLOWED_MIME_TYPES = env.list(
    "IMPORT_FILES_ALLOWED_MIME_TYPES",
    default=[
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
)

# https://pypi.org/project/django-admin-env-notice/
ENVIRONMENT_NAME = env.str("ENVIRONMENT_NAME", default="")
ENVIRONMENT_COLOR = env.str("ENVIRONMENT_COLOR", default="")
ENVIRONMENT_TEXT_COLOR = env.str("ENVIRONMENT_TEXT_COLOR", default="#ffffff")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "main_formatter": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s "
            "(%(filename)s:%(lineno)d)",
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

# Sentry
SENTRY_DSN = env.str("SENTRY_DSN", default="")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT_NAME,
        integrations=[DjangoIntegration(), LoggingIntegration()],
    )


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
            "SHOW_COLLAPSED": True,
            "SHOW_TOOLBAR_CALLBACK": f"{__name__}.show_toolbar",
        }

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
            "OPTIONS": {"min_length": 4},
        }
    ]

    if DEBUG:
        MIDDLEWARE.append("request_logging.middleware.LoggingMiddleware")

    REQUEST_LOGGING_DATA_LOG_LEVEL = logging.INFO
    REQUEST_LOGGING_MAX_BODY_LENGTH = 1000
