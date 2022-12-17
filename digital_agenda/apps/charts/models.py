from ckeditor.fields import RichTextField
from composite_field import CompositeField
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
    image = models.ImageField(
        blank=True,
        help_text="Thumbnail image for this Chart Group. A placeholder will be used if this is not configured.",
    )

    indicator_group_label = models.CharField(max_length=60, default="Indicator group")
    indicator_label = models.CharField(max_length=60, default="Indicator")
    breakdown_group_label = models.CharField(max_length=60, default="Breakdown group")
    breakdown_label = models.CharField(max_length=60, default="Breakdown")
    period_label = models.CharField(max_length=60, default="Period")
    unit_label = models.CharField(max_length=60, default="Unit of measure")

    indicator_groups = models.ManyToManyField("core.IndicatorGroup")
    periods = models.ManyToManyField(
        "core.Period",
        db_table="chart_group_periods",
        help_text=(
            "Limit chart group to the specified periods. If none are specified ALL "
            "available periods are used instead."
        ),
        blank=True,
    )

    class Meta:
        db_table = "chart_groups"
        ordering = ["display_order", "code"]

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return f"[{self.code}] {self.short_name}"


def filter_option_field(rel_model):
    class FilterOptionField(CompositeField):
        hidden = models.BooleanField(
            default=False, help_text="Force hide the filter for this chart."
        )
        defaults = models.ManyToManyField(
            rel_model,
            related_name="default_charts",
            blank=True,
            help_text=(
                "Multiple defaults can be specified, however only valid choices depending on the other filters "
                "will be used."
            ),
        )
        ignored = models.ManyToManyField(
            rel_model,
            related_name="ignored_charts",
            blank=True,
            help_text="Values specified here will be hidden and not available for selection.",
        )

    return FilterOptionField()


class Chart(DraftModel, TimestampedModel, DisplayOrderModel):
    # !IMPORTANT WARNING!
    #
    # When adding an entry here a corresponding entry must be added in
    #
    #  - frontend/src/lib/chartRegistry.js
    #  - frontend/src/lib/chartDefaultImages.js
    #
    CHART_TYPE_CHOICES = [
        (
            "Column",
            (
                ("COLUMN_COMPARE_COUNTRIES", "Column Chart: Compare Countries"),
                ("COLUMN_COMPARE_BREAKDOWNS", "Column Chart: Compare Breakdowns"),
                (
                    "COLUMN_STACKED_COMPARE_BREAKDOWNS",
                    "Column Chart Stacked: Compare Breakdowns",
                ),
                (
                    "COLUMN_STACKED_COMPARE_BREAKDOWNS_WEIGHTED",
                    "Column Chart Stacked: Compare Breakdowns Weighted",
                ),
            ),
        ),
        (
            "Spline",
            (
                ("SPLINE_COMPARE_COUNTRIES", "Spline Chart: Compare Countries"),
                ("SPLINE_COMPARE_BREAKDOWNS", "Spline Chart: Compare Breakdowns"),
                (
                    "SPLINE_COMPARE_TWO_INDICATORS",
                    "Spline Chart: Compare Two Indicators",
                ),
            ),
        ),
        (
            "Scatter",
            (
                (
                    "SCATTER_COMPARE_TWO_INDICATORS",
                    "Scatter Chart: Compare Two Indicators",
                ),
            ),
        ),
        (
            "Bubble",
            (
                (
                    "BUBBLE_COMPARE_THREE_INDICATORS",
                    "Bubble Chart: Compare Three Indicators",
                ),
            ),
        ),
        (
            "Map",
            (
                (
                    "MAP_COMPARE_COUNTRIES",
                    "Map Chart: Compare Countries",
                ),
            ),
        ),
        (
            "Table",
            (
                (
                    "TABLE_DEBUG_DATA",
                    "Table: Debug Data",
                ),
            ),
        ),
    ]

    chart_group = models.ForeignKey("ChartGroup", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.SlugField(unique=True)

    chart_type = models.CharField(max_length=50, choices=CHART_TYPE_CHOICES)
    description = RichTextField()
    image = models.ImageField(
        blank=True,
        help_text=(
            "Custom thumbnail image to use for this chart. If not set, a default one will be used "
            "depending on the chart type."
        ),
    )

    indicator_group_filter = filter_option_field("core.IndicatorGroup")
    indicator_filter = filter_option_field("core.Indicator")
    breakdown_group_filter = filter_option_field("core.BreakdownGroup")
    breakdown_filter = filter_option_field("core.Breakdown")
    period_filter = filter_option_field("core.Period")
    unit_filter = filter_option_field("core.Unit")
    country_filter = filter_option_field("core.Country")

    class Meta:
        db_table = "charts"
        ordering = ["display_order", "code"]

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return self.name

    @classmethod
    @property
    def m2m_filter_options(cls):
        return tuple(
            subfield.name
            for private_field in Chart._meta.private_fields
            for subfield in private_field.subfields.values()
            if isinstance(subfield, models.ManyToManyField)
        )

    @classmethod
    @property
    def filter_options(cls):
        return tuple(
            subfield.name
            for private_field in Chart._meta.private_fields
            for subfield in private_field.subfields.values()
        )
