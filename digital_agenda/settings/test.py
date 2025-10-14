from .base import *

# Disable caches while running tests
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Betamax settings
# =============
from betamax import Betamax

BETAMAX_FIXTURES = str(BASE_DIR / "fixtures" / "test_betamax")

with Betamax.configure() as config:
    config.cassette_library_dir = BETAMAX_FIXTURES
    config.default_cassette_options["record_mode"] = "once"
    config.default_cassette_options["preserve_exact_body_bytes"] = "all"

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: False,
}