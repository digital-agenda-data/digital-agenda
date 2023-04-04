import zoneinfo

from django.conf import settings
from django.utils import timezone


# See https://docs.djangoproject.com/en/4.1/topics/i18n/timezones/#get-current-timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.COOKIES.get(settings.TIMEZONE_COOKIE)
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
