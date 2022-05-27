from django.db import models
from django.contrib.postgres.fields import CICharField
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property


from digital_agenda.common.models import TimestampedModel


class BaseLabeledModel(TimestampedModel):
    label = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class DatasetManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code__iexact=code)


class Dataset(BaseLabeledModel):

    code = CICharField(max_length=60, unique=True)

    objects = DatasetManager()

    class Meta:
        db_table = "estat_datasets"

    def natural_key(self):
        return (self.code,)  # noqa

    def __str__(self):
        return self.code

    def dimension(self, code):
        try:
            return self.dimensions.get(code=code)
        except Dimension.DoesNotExist:
            return None

    @cached_property
    def single_valued_dimensions(self):
        return [dim for dim in self.dimensions.all() if dim.single_valued]


class DimensionManager(models.Manager):
    def get_by_natural_key(self, dataset_code, code):
        return self.get(dataset__code=dataset_code, code=code)


class Dimension(BaseLabeledModel):

    SURROGATE_CODE = "~SURROGATE~"

    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="dimensions"
    )
    code = CICharField(max_length=60)

    objects = DimensionManager()

    class Meta:
        db_table = "estat_dimensions"

    def __str__(self):
        return self.code

    def natural_key(self):
        return (self.code,) + self.dataset.natural_key()

    @cached_property
    def single_filtered_value(self):
        if self.values.count() > self.values.filter(enabled=True).count() == 1:
            return self.values.get(enabled=True)

        return None


class DimensionValueManager(models.Manager):
    def get_by_natural_key(self, dataset_code, dimension_code, code):
        return self.get(
            dataset__dimension__code=dataset_code,
            dimension__code=dimension_code,
            code=code,
        )


class DimensionValue(BaseLabeledModel):

    dimension = models.ForeignKey(
        "Dimension", on_delete=models.CASCADE, related_name="values"
    )
    code = CICharField(max_length=60)
    enabled = models.BooleanField(default=True)

    objects = DimensionValueManager()

    class Meta:
        db_table = "estat_dim_values"
        unique_together = ("dimension", "code")

    def __str__(self):
        return self.code

    def natural_key(self):
        return (self.code,) + self.dimension.natural_key()


class DatasetConfigManager(models.Manager):
    def get_by_natural_key(self, dataset_code):
        return self.get(dataset__code=dataset_code)


class DatasetConfig(TimestampedModel):

    dataset = models.OneToOneField(
        "Dataset", on_delete=models.CASCADE, primary_key=True, related_name="config"
    )
    indicator = models.ForeignKey(
        "Dimension",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    indicator_surrogate = models.ForeignKey(
        "DimensionValue",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    breakdown = models.ForeignKey(
        "Dimension",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    breakdown_surrogate = models.ForeignKey(
        "DimensionValue",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    unit = models.ForeignKey(
        "Dimension",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    unit_surrogate = models.ForeignKey(
        "DimensionValue",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    country = models.ForeignKey(
        "Dimension",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    country_surrogate = models.ForeignKey(
        "DimensionValue",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    period = models.ForeignKey(
        "Dimension",
        related_name="+",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    period_surrogate = models.ForeignKey(
        "DimensionValue",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    objects = DatasetConfigManager()

    class Meta:
        db_table = "estat_dataset_configs"

    def __str__(self):
        return self.dataset.code

    def natural_key(self):
        return (self.dataset.code,)  # noqa

    def clean(self):
        for dimension in ("indicator", "breakdown", "unit", "country", "period"):
            if (
                getattr(self, dimension)
                and getattr(self, dimension).code == Dimension.SURROGATE_CODE
                and not getattr(self, f"{dimension}_surrogate")
            ):
                raise ValidationError(
                    f"Must provide a surrogate value for {dimension}."
                )
            elif (
                getattr(self, dimension)
                and getattr(self, dimension).code != Dimension.SURROGATE_CODE
                and getattr(self, f"{dimension}_surrogate")
            ):
                raise ValidationError(
                    f"Cannot set a surrogate value for {dimension} when dimension is not surrogate."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def has_dimension(self, dimension):
        return (
            self.indicator == dimension
            or self.breakdown == dimension
            or self.unit == dimension
            or self.country == dimension
            or self.period == dimension
        )


class Fact(TimestampedModel):
    value = models.FloatField(null=True, blank=True)
    flags = models.CharField(max_length=2, blank=True)
    dataset = models.ForeignKey(
        "Dataset", on_delete=models.CASCADE, related_name="facts"
    )
    indicator = models.ForeignKey(
        "DimensionValue", on_delete=models.CASCADE, related_name="+"
    )
    breakdown = models.ForeignKey(
        "DimensionValue", on_delete=models.CASCADE, related_name="+"
    )
    unit = models.ForeignKey(
        "DimensionValue", on_delete=models.CASCADE, related_name="+"
    )
    country = models.ForeignKey(
        "DimensionValue", on_delete=models.CASCADE, related_name="+"
    )
    period = models.ForeignKey(
        "DimensionValue", on_delete=models.CASCADE, related_name="+"
    )

    class Meta:
        db_table = "estat_facts"
        unique_together = (
            "dataset",
            "indicator",
            "breakdown",
            "unit",
            "country",
            "period",
        )
        constraints = [
            models.CheckConstraint(
                check=models.Q(value__isnull=False) | ~models.Q(flags=""),
                name="estat_fact_either_val_or_flags",
            ),
        ]
