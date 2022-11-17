from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import CICharField
from django.db import models

from digital_agenda.common.models import DisplayOrderModel
from digital_agenda.common.models import TimestampedModel


class ChartGroupIndicatorLinkManager(models.Manager):
    def get_by_natural_key(self, indicator_group_code, chart_group_code):
        return self.get(
            indicator_group_code=indicator_group_code, chart_group_code=chart_group_code
        )


class ChartGroupIndicatorLink(DisplayOrderModel):
    indicator_group = models.ForeignKey("core.IndicatorGroup", on_delete=models.CASCADE)
    chart_group = models.ForeignKey("ChartGroup", on_delete=models.CASCADE)

    objects = ChartGroupIndicatorLinkManager()

    class Meta:
        db_table = "chart_group_links"
        unique_together = ("indicator_group", "chart_group")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.chart_group} -> {self.indicator_group}"

    def natural_key(self):
        return self.indicator_group.code, self.chart_group.code


class ChartGroup(TimestampedModel, DisplayOrderModel):
    is_draft = models.BooleanField(
        default=False, help_text="Draft items will only be visible for admins."
    )
    code = CICharField(max_length=60, unique=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=40)
    description = RichTextField()
    image = models.ImageField(blank=True)

    periods = models.ManyToManyField(
        "core.Period",
        db_table="chart_group_periods",
        help_text=(
            "Limit chart group to the specified periods. If none are specified ALL "
            "available periods are used instead."
        ),
        blank=True,
    )
    indicator_groups = models.ManyToManyField(
        "core.IndicatorGroup", through="ChartGroupIndicatorLink"
    )

    class Meta:
        db_table = "chart_groups"
        ordering = ["display_order", "code"]

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return f"[{self.code}] {self.short_name}"
