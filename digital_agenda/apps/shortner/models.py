import functools

from django.conf import settings
from django.db import models
from hashid_field import BigHashidAutoField

from digital_agenda.common.models import TimestampedModel


class ShortURL(TimestampedModel):
    id = BigHashidAutoField(primary_key=True)
    chart = models.ForeignKey("charts.Chart", on_delete=models.CASCADE)
    query_arguments = models.CharField(max_length=1024, blank=True, default="")

    class Meta:
        unique_together = ("chart", "query_arguments")

    @functools.cached_property
    def chart_url(self):
        protocol = "https" if settings.HAS_HTTPS else "http"
        host = settings.FRONTEND_HOST[0]
        args = self.query_arguments.strip("?")

        return (
            f"{protocol}://{host}/datasets/"
            f"{self.chart.chart_group.code}/charts/{self.chart.code}?{args}"
        )
