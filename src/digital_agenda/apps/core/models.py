from django.db import models
from django.contrib.postgres.fields import CICharField
from django.core.exceptions import ValidationError


class DataSource(models.Model):
    """
    Data sources, e.g. Eurostat
    """

    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "data_sources"

    def __str__(self):
        return self.name


class DataSourceReference(models.Model):
    """
    Data source references, e.g. a dataset from Eurostat
    """

    data_source = models.ForeignKey(
        "DataSource", on_delete=models.CASCADE, related_name="references"
    )
    name = models.CharField(max_length=200)
    url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "data_source_refs"
        unique_together = ("data_source", "name")

    def __str__(self):
        return self.name


class BaseDimensionManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class BaseDimensionModel(models.Model):

    """
    Base model for dimension-like models, with a unique code and label/short label fields.
    """

    code = CICharField(max_length=60, unique=True)
    label = models.TextField(null=True, blank=True)
    alt_label = models.TextField(null=True, blank=True, verbose_name="Alt. label")

    objects = BaseDimensionManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        if self.label:
            return f"[{self.code}] {self.label}"
        elif self.alt_label:
            return f"[{self.code}] {self.alt_label}"
        else:
            return self.code


class IndicatorGroup(BaseDimensionModel):

    """
    Model for groups of indicators. Groups are not referenced directly by facts,
    and function as a hierarchical dimension table.
    """

    indicators = models.ManyToManyField(
        "Indicator", related_name="groups", db_table="indicators_groups"
    )

    class Meta:
        db_table = "indicator_groups"


class Indicator(BaseDimensionModel):
    """Dimension model for indicators"""

    data_source_ref = models.ForeignKey(
        "DataSourceReference", on_delete=models.CASCADE, related_name="indicators"
    )
    definition = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    breakdowns = models.ManyToManyField(
        "Breakdown", related_name="indicators", db_table="indicators_breakdowns"
    )
    units = models.ManyToManyField(
        "Unit", related_name="indicators", db_table="indicators_units"
    )
    countries = models.ManyToManyField(
        "Country", related_name="indicators", db_table="indicators_countries"
    )
    periods = models.ManyToManyField(
        "Period", related_name="indicators", db_table="indicators_periods"
    )

    class Meta:
        db_table = "indicators"


class BreakdownGroup(BaseDimensionModel):

    """
    Model for groups of breakdowns.
    """

    breakdowns = models.ManyToManyField(
        "Breakdown", related_name="groups", db_table="breakdowns_groups"
    )

    class Meta:
        db_table = "breakdown_groups"


class Breakdown(BaseDimensionModel):
    """Dimension model for secondary dimensions, a.k.a. breakdowns."""

    class Meta:
        db_table = "breakdowns"


class Unit(BaseDimensionModel):
    """Dimension model for measure units"""

    class Meta:
        db_table = "units"


class Country(BaseDimensionModel):
    """Dimension model for countries / country group entities."""

    class Meta:
        db_table = "countries"
        verbose_name_plural = "Countries"


class Period(BaseDimensionModel):
    """Dimension model for time periods"""

    class Meta:
        db_table = "periods"


class Fact(models.Model):
    """
    The facts table, center of the star schema.
    """

    value = models.FloatField(null=True, blank=True)
    flags = models.CharField(max_length=2, blank=True)
    indicator = models.ForeignKey(
        "Indicator", on_delete=models.CASCADE, related_name="facts"
    )
    breakdown = models.ForeignKey(
        "Breakdown", on_delete=models.CASCADE, related_name="facts"
    )
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE, related_name="facts")
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="facts"
    )
    period = models.ForeignKey("Period", on_delete=models.CASCADE, related_name="facts")

    class Meta:
        db_table = "facts"
        unique_together = ("indicator", "breakdown", "unit", "country", "period")
        constraints = [
            models.CheckConstraint(
                check=models.Q(value__isnull=False) | ~models.Q(flags=""),
                name="core_fact_either_val_or_flags",
            )
        ]

    def clean(self):
        if self.indicator not in self.breakdown.indicators:
            raise ValidationError("Indicator does not match breakdown")
        elif self.indicator not in self.unit.indicators:
            raise ValidationError("Indicator does not match unit")
        elif self.indicator not in self.country.indicators:
            raise ValidationError("Indicator does not match country")
        elif self.indicator not in self.period.indicators:
            raise ValidationError("Indicator does not match period")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
