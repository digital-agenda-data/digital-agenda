from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


def reverse_absolute_uri(*args, **kwargs):
    """Just like django reverse, but get a fully qualified URL instead"""
    return urljoin(
        settings.PROTOCOL + settings.BACKEND_HOST[0], reverse(*args, **kwargs)
    )


def split_email(value):
    return [i.strip() for i in value.split(",") if i.strip()]
