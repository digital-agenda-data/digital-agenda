import os

from celery import Celery
from celery.app import trace

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digital_agenda.settings.prod")

app = Celery("digital_agenda")

# Remove task result from log
trace.LOG_SUCCESS = "Task %(name)s[%(id)s] succeeded in %(runtime)ss"

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
