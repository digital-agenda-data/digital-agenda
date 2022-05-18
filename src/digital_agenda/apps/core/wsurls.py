from django.urls import re_path

from . import wsconsumers

ws_urlpatterns = [
    re_path(r"ws/test/$", wsconsumers.Test),
    re_path(r"ws/health/$", wsconsumers.HealthCheck),
]
