import functools

from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from composite_field import CompositeField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import strip_tags
from hashid_field import BigHashidAutoField

from digital_agenda.apps.core.models import Fact
from digital_agenda.common.citext import CICharField
from digital_agenda.common.models import DisplayOrderModel
from digital_agenda.common.models import NaturalCodeManger
from digital_agenda.common.models import TimestampedModel


class DraftModel(models.Model):
    is_draft = models.BooleanField(
        default=False, help_text="Draft items will only be visible for admins."
    )

    class Meta:
        abstract = True


class ChartGroup(DraftModel, TimestampedModel, DisplayOrderModel):
    objects = NaturalCodeManger()

    code = CICharField(max_length=60, unique=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=40)
    license = RichTextField()
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

    period_start = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Limit chart group to the specific periods greater than or equal to this year",
        validators=[MinValueValidator(settings.MIN_YEAR)],
    )
    period_end = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Limit chart group to the specific periods less than or equal to this year",
        validators=[MinValueValidator(settings.MIN_YEAR)],
    )
    indicator_groups = models.ManyToManyField("core.IndicatorGroup")

    class Meta:
        ordering = ["display_order", "code"]

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return f"[{self.code}] {self.short_name}"

    def clean(self):
        if (
            self.period_start
            and self.period_end
            and self.period_start > self.period_end
        ):
            error = "Start period must be less than or equal to the end period"
            raise ValidationError({"period_start": error, "period_end": error})

    def get_label(self, dimension):
        return getattr(self, dimension + "_label", dimension.title())

    @property
    def facts(self):
        return Fact.objects.filter(indicator__groups__chartgroup=self).distinct()


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


class ChartManger(models.Manager):
    def get_by_natural_key(self, chart_group_code, code):
        return self.get(chart_group__code=chart_group_code, code=code)


class Chart(DraftModel, TimestampedModel, DisplayOrderModel):
    objects = ChartManger()
    # !IMPORTANT WARNING!
    #
    # When adding an entry here, a corresponding entry must be added in
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
            "Bar",
            (
                ("BAR_COMPARE_COUNTRIES", "Bar Chart: Compare Countries"),
                ("BAR_COMPARE_BREAKDOWNS", "Bar Chart: Compare Breakdowns"),
                (
                    "BAR_STACKED_COMPARE_BREAKDOWNS",
                    "Bar Chart Stacked: Compare Breakdowns",
                ),
                (
                    "BAR_STACKED_COMPARE_BREAKDOWNS_WEIGHTED",
                    "Bar Chart Stacked: Compare Breakdowns Weighted",
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
        ("EU Map", (("MAP_EU_COMPARE_COUNTRIES", "EU Map Chart: Compare Countries"),)),
        (
            "World Map",
            (("MAP_WORLD_COMPARE_COUNTRIES", "World Map Chart: Compare Countries"),),
        ),
        ("Table", (("TABLE_DEBUG_DATA", "Table: Debug Data"),)),
    ]

    id = BigHashidAutoField(primary_key=True)
    chart_group = models.ForeignKey("ChartGroup", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=255)

    chart_type = models.CharField(max_length=50, choices=CHART_TYPE_CHOICES)
    description = RichTextField()
    image = models.ImageField(
        blank=True,
        help_text=(
            "Custom thumbnail image to use for this chart. If not set, a default one will be used "
            "depending on the chart type."
        ),
    )

    min_value = models.FloatField(
        help_text="Minimum value of the axis", default=None, null=True, blank=True
    )
    max_value = models.FloatField(
        help_text="Maximum value of the axis", default=None, null=True, blank=True
    )

    indicator_group_filter = filter_option_field("core.IndicatorGroup")
    indicator_filter = filter_option_field("core.Indicator")
    breakdown_group_filter = filter_option_field("core.BreakdownGroup")
    breakdown_filter = filter_option_field("core.Breakdown")
    period_filter = filter_option_field("core.Period")
    unit_filter = filter_option_field("core.Unit")
    country_filter = filter_option_field("core.Country")

    legend_layout = models.CharField(
        max_length=20,
        default=None,
        null=True,
        blank=True,
        help_text="Choose default legend layout type",
        choices=[("horizontal", "horizontal"), ("vertical", "vertical")],
    )

    class Meta:
        ordering = ["display_order", "code"]
        unique_together = ("chart_group", "code")

    def natural_key(self):
        return (self.chart_group.code, self.code)  # noqa

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

    @functools.cached_property
    def plaintext_description(self):
        return strip_tags(self.description)

    def clean(self):
        if (
            self.min_value is not None
            and self.max_value is not None
            and self.min_value >= self.max_value
        ):
            msg = "Min value must be lower than the Max value"
            raise ValidationError({"min_value": msg, "max_value": msg})


class ChartOptionBaseModel(TimestampedModel):
    color = ColorField(
        help_text="Color used for this indicator chart series",
        blank=True,
        null=True,
        default=None,
    )
    dash_style = models.CharField(
        max_length=20,
        help_text="https://api.highcharts.com/highcharts/plotOptions.spline.dashStyle",
        blank=True,
        null=True,
        default=None,
        choices=[
            ("Dash", "Dash"),
            ("DashDot", "DashDot"),
            ("Dot", "Dot"),
            ("LongDash", "LongDash"),
            ("LongDashDot", "LongDashDot"),
            ("LongDashDotDot", "LongDashDotDot"),
            ("ShortDash", "ShortDash"),
            ("ShortDashDot", "ShortDashDot"),
            ("ShortDashDotDot", "ShortDashDotDot"),
            ("ShortDot", "ShortDot"),
            ("Solid", "Solid"),
        ],
    )
    symbol = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default=None,
        help_text="https://api.highcharts.com/highcharts/plotOptions.spline.marker.symbol",
        choices=[
            ("circle", "circle"),
            ("square", "square"),
            ("diamond", "diamond"),
            ("triangle", "triangle"),
            ("triangle-down", "triangle-down"),
        ],
    )
    custom_symbol = models.ImageField(
        blank=True,
        null=True,
        default=None,
        help_text="Custom symbol used instead of the predefined ones",
    )

    class Meta:
        abstract = True

    def clean(self):
        if self.symbol and self.custom_symbol:
            error = "Symbol and Custom Symbol cannot be used at the same time"
            raise ValidationError({"symbol": error, "custom_symbol": error})


class IndicatorChartOption(ChartOptionBaseModel):
    indicator = models.OneToOneField(
        "core.Indicator", on_delete=models.CASCADE, related_name="chart_options"
    )


class BreakdownChartOption(ChartOptionBaseModel):
    breakdown = models.OneToOneField(
        "core.Breakdown", on_delete=models.CASCADE, related_name="chart_options"
    )


class ExtraChartNote(TimestampedModel):
    indicator = models.ForeignKey(
        "core.Indicator", on_delete=models.CASCADE, related_name="extra_notes"
    )
    period = models.ForeignKey("core.Period", on_delete=models.CASCADE)
    note = models.CharField(
        max_length=255, help_text="Extra notes to show in the chart"
    )


class ChartFilterOrder(DisplayOrderModel):
    class FilterTypes(models.TextChoices):
        INDICATOR_GROUP = "indicatorGroup", "Indicator Group"
        INDICATOR = "indicator", "Indicator"
        BREAKDOWN_GROUP = "breakdownGroup", "Breakdown Group"
        BREAKDOWN = "breakdown", "Breakdown"
        PERIOD = "period", "Period"
        UNIT = "unit", "Unit"
        COUNTRY = "country", "Country"

    chart = models.ForeignKey(
        Chart, on_delete=models.CASCADE, related_name="filter_order"
    )
    filter_field = models.CharField(
        max_length=50,
        choices=FilterTypes.choices,
        help_text=(
            "Order of the filter in the chart. "
            "Filters not specified here will use the default order. "
            "Filters that are not used in the chart will be ignored."
        ),
    )

    class Meta:
        ordering = ["display_order"]
        unique_together = ("chart", "filter_field")
        verbose_name = "Chart Filter Order"
        verbose_name_plural = "Chart Filters Order"
