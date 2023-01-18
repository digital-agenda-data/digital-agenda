from django.contrib.postgres.fields import CICharField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.db import models

MIN_YEAR = 1990


class GeoGroup(models.Model):
    code = CICharField(max_length=60, unique=True)
    size = models.PositiveIntegerField()
    note = models.CharField(max_length=1024, blank=True, null=True)
    geo_codes = models.JSONField(default=list)

    def __str__(self):
        return self.code

    def clean(self):
        try:
            assert isinstance(self.geo_codes, list)
            assert len(self.geo_codes) > 0
            assert all(isinstance(code, str) for code in self.geo_codes)
        except AssertionError:
            raise ValidationError(
                {"geo_codes": ValidationError("Must be a non-empty Array of strings")}
            )

        if len(set(self.geo_codes)) != len(self.geo_codes):
            raise ValidationError(
                {"geo_codes": ValidationError("No duplicate codes allowed")}
            )

        if len(self.geo_codes) != self.size:
            raise ValidationError(
                {
                    "size": ValidationError(
                        f"Size mismatch; geo codes has {len(self.geo_codes)} codes"
                    )
                }
            )


def default_mappings():
    return {
        "indicator": {},
        "breakdown": {},
        "country": {},
        "unit": {},
        "period": {},
    }


class ImportConfig(models.Model):
    code = CICharField(max_length=60)
    title = models.CharField(max_length=1024, blank=True, null=True)
    last_import_time = models.TimeField(null=True)

    indicator = CICharField(max_length=60)
    indicator_is_surrogate = models.BooleanField(default=False)

    breakdown = CICharField(max_length=60)
    breakdown_is_surrogate = models.BooleanField(default=False)

    country = CICharField(max_length=60, default="geo")
    country_is_surrogate = models.BooleanField(default=False)

    unit = CICharField(max_length=60, default="unit")
    unit_is_surrogate = models.BooleanField(default=False)

    period = CICharField(max_length=60, default="time")
    period_is_surrogate = models.BooleanField(default=False)

    period_start = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Only include datapoints for periods greater than or equal to this year",
        validators=[MinValueValidator(MIN_YEAR)],
    )
    period_end = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Only include datapoints for periods less than or equal to this year",
        validators=[MinValueValidator(MIN_YEAR)],
    )
    country_group = models.ForeignKey(
        GeoGroup,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Only include datapoints for countries in this group OR the group itself",
    )
    filters = models.JSONField(default=dict, blank=True)
    mappings = models.JSONField(default=default_mappings, blank=True)
    status = models.TextField()

    def clean(self):
        for attr in ("code", "indicator", "breakdown", "country", "unit", "period"):
            setattr(self, attr, getattr(self, attr).lower())

        if (
            self.period_start
            and self.period_end
            and self.period_start > self.period_end
        ):
            error = ValidationError(
                "Start period must be less than or equal to the end period"
            )
            raise ValidationError(
                {
                    "period_start": error,
                    "period_end": error,
                }
            )

        if not isinstance(self.filters, dict):
            raise ValidationError({"filters": "Must be a valid JSON object"})

        if not isinstance(self.mappings, dict):
            raise ValidationError({"mappings": "Must be a valid JSON object"})

        if invalid := set(self.mappings).difference(set(default_mappings())):
            raise ValidationError({"mappings": f"Invalid mappings: {tuple(invalid)}"})

        for key, value in self.mappings.items():
            if not isinstance(value, dict):
                raise ValidationError(
                    {"mappings": f"Invalid mapping {key!r}: must be a JSON object"}
                )

    def __str__(self):
        if self.title:
            return f"{self.code} ({self.pk}) {self.title}"
        return f"{self.code} ({self.pk})"
