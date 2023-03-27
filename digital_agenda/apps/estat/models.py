import collections
from functools import cached_property

from django.conf import settings
from django.contrib.postgres.fields import CICharField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.db import models
from django_task.models import TaskRQ

from digital_agenda.common.models import NaturalCodeManger


class GeoGroup(models.Model):
    code = CICharField(max_length=60, unique=True)
    size = models.PositiveIntegerField()
    note = models.CharField(max_length=1024, blank=True, null=True)
    geo_codes = models.JSONField(default=list)

    objects = NaturalCodeManger()

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

    def natural_key(self):
        return (self.code,)  # noqa


def default_mappings():
    return {
        "indicator": {},
        "breakdown": {},
        "country": {},
        "unit": {},
        "period": {},
    }


def is_unique(values):
    return len(values) == len(set(v.lower() for v in values))


class ImportConfig(models.Model):
    code = CICharField(max_length=60)
    title = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=(
            "Human readable title for logging and differentiating from multiple configs for the same dataset"
        ),
    )

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
        validators=[MinValueValidator(settings.MIN_YEAR)],
    )
    period_end = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Only include datapoints for periods less than or equal to this year",
        validators=[MinValueValidator(settings.MIN_YEAR)],
    )
    country_group = models.ForeignKey(
        GeoGroup,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Only include datapoints for countries in this group OR the group itself",
    )
    filters = models.JSONField(
        default=dict,
        blank=True,
        help_text="Object with ESTAT dimension keys and an Array of accepted codes as values.",
    )
    mappings = models.JSONField(
        default=default_mappings,
        blank=True,
        help_text="Define how ESTAT codes are transformed before inserting into the DB",
    )

    @cached_property
    def ci_filters(self):
        """Convert the filters specified in the import config into lower-cased
        sets, to be used for case insensitive checks.
        """
        result = collections.defaultdict(set)

        for key, values in self.filters.items():
            result[key.lower()].update([val.lower() for val in values])

        # Update the "country" dimension filter (usually geo) with
        # the configured country group filter if available.
        if self.country_group:
            result[self.country.lower()].update(
                val.lower() for val in self.country_group.geo_codes
            )
            result[self.country.lower()].add(self.country_group.code.lower())

        return result

    @cached_property
    def ci_mappings(self):
        result = collections.defaultdict(dict)

        for dimension, mapping in self.mappings.items():
            for original, new_value in mapping.items():
                result[dimension.lower()][original.lower()] = new_value.lower()
        return result

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

        if not is_unique(self.filters):
            raise ValidationError({"filters": "Duplicate keys detected"})

        for key, values in self.filters.items():
            if not is_unique(values):
                raise ValidationError(
                    {"filters": f"Duplicate values detected for the {key!r} dimension"}
                )

        if not isinstance(self.mappings, dict):
            raise ValidationError({"mappings": "Must be a valid JSON object"})

        for key, values in self.mappings.items():
            if not isinstance(values, dict):
                raise ValidationError(
                    {
                        "mappings": f"Invalid mapping {key!r}: Must be a valid JSON object"
                    }
                )

        if not is_unique(self.mappings):
            raise ValidationError({"mappings": "Duplicate keys detected"})

        if invalid := set(self.mappings).difference(set(default_mappings())):
            raise ValidationError({"mappings": f"Invalid mappings: {tuple(invalid)}"})

        for key, values in self.mappings.items():
            if not is_unique(values):
                raise ValidationError(
                    {"mappings": f"Duplicate values detected for the {key!r} dimension"}
                )

    def clean_with_dataset(self, dataset):
        """Simple sanity checks to validate the data matches the given config."""
        for key, values in self.ci_filters.items():
            if key not in dataset.dimension_ids:
                raise ValidationError(
                    f"Invalid filter {key!r}, no dimensions with that id found in: "
                    f"{dataset.dimension_ids}"
                )

            categories = dataset.dimension_dict[key]
            for val in values:
                if val not in categories:
                    raise ValidationError(
                        f"Filter value for {key!r} not found: {val!r}"
                    )
        for dimension in ("indicator", "breakdown", "country", "unit", "period"):
            config_dim = getattr(self, dimension)
            is_surrogate = getattr(self, f"{dimension}_is_surrogate")

            if is_surrogate:
                # No point in checking surrogates since they are hardcoded values
                continue

            if config_dim not in dataset.dimension_ids:
                raise ValidationError(
                    f"Invalid dimension {config_dim!r}, no dimensions with that id found in: "
                    f"{dataset.dimension_ids}"
                )

            mappings = self.ci_mappings.get(dimension, {})
            categories = dataset.dimension_dict[config_dim]
            for val in mappings.keys():
                if val not in categories:
                    raise ValidationError(
                        f"Mapped value for {dimension!r} not found: {val!r}"
                    )

    def run_import(self, **kwargs):
        return self._run_import(False, **kwargs)

    def queue_import(self, **kwargs):
        return self._run_import(True, **kwargs)

    def _run_import(self, is_async, **kwargs):
        task = ImportFromConfigTask.objects.create(import_config=self, **kwargs)
        task.run(is_async=is_async)
        return task

    @cached_property
    def latest_task(self):
        try:
            return self.tasks.latest()
        except ImportFromConfigTask.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.code} ({self.pk})"


class ImportFromConfigTask(TaskRQ):
    DEFAULT_VERBOSITY = 2
    TASK_QUEUE = "default"
    TASK_TIMEOUT = 30 * 60
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    import_config = models.ForeignKey(
        ImportConfig, on_delete=models.CASCADE, related_name="tasks"
    )
    force_download = models.BooleanField(
        default=False, help_text="Force redownload the dataset"
    )
    delete_existing = models.BooleanField(
        default=False,
        help_text="Delete facts linked to this import config before starting the import",
    )
    task_verbosity = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=DEFAULT_VERBOSITY,
        choices=(
            (0, "NONE"),
            (1, "WARNING"),
            (2, "INFO"),
            (3, "DEBUG"),
        ),
    )

    class Meta:
        get_latest_by = "created_on"
        verbose_name = "Import config result"
        verbose_name_plural = "Import configs results"

    @staticmethod
    def get_jobclass():
        from .jobs import ImportFromConfigJob

        return ImportFromConfigJob
