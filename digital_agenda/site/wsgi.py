import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digital_agenda.settings")
os.environ.setdefault("SERVER_GATEWAY", "wsgi")

application = get_wsgi_application()
