import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from digital_agenda.apps.core.wsurls import ws_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digital_agenda.settings")

django.setup()

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
    }
)
