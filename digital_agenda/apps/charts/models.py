from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import CICharField
from django.db import models

from digital_agenda.common.models import DisplayOrderModel
from digital_agenda.common.models import TimestampedModel


class DraftModel(models.Model):
    is_draft = models.BooleanField(
        default=False, help_text="Draft items will only be visible for admins."
    )

    class Meta:
        abstract = True


class ChartGroup(DraftModel, TimestampedModel, DisplayOrderModel):

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
    indicator_groups = models.ManyToManyField("core.IndicatorGroup")

    class Meta:
        db_table = "chart_groups"
        ordering = ["display_order", "code"]

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return f"[{self.code}] {self.short_name}"


class Chart(DraftModel, TimestampedModel, DisplayOrderModel):
    CHART_TYPE_CHOICES = [
        (
            "Column",
            (
                ("COLUMN_COMPARE_COUNTRIES", "Column Chart: Compare Countries"),
                ("COLUMN_COMPARE_BREAKDOWNS", "Column Chart: Compare Breakdowns"),
            ),
        ),
    ]

    chart_group = models.ForeignKey("ChartGroup", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.SlugField(unique=True)

    chart_type = models.CharField(max_length=50, choices=CHART_TYPE_CHOICES)
    description = RichTextField()

    class Meta:
        db_table = "charts"
        ordering = ["display_order", "code"]

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return self.name
