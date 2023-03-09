import functools

from django.conf import settings
from django.db import models
from hashid_field import BigHashidAutoField

from digital_agenda.common.models import TimestampedModel


class ShortURL(TimestampedModel):
    id = BigHashidAutoField(primary_key=True)
    chart = models.ForeignKey("charts.Chart", on_delete=models.CASCADE)
    query_arguments = models.CharField(max_length=1024, blank=True, default="")

    @functools.cached_property
    def chart_url(self):
        protocol = "https" if settings.HAS_HTTPS else "http"
        host = settings.FRONTEND_HOST[0]

        return (
            f"{protocol}://{host}/datasets/"
            f"{self.chart.chart_group.code}/charts/{self.chart.code}?{self.query_arguments}"
        )
