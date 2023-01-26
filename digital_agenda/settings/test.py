from .base import *

# Disable caches while running tests
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
