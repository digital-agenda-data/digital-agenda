from .base import *

# Disable caches while running tests
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
