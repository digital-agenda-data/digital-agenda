import collections
from functools import cached_property

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.db import models
from django_task.models import TaskRQ
from sympy import sympify, symbols

from digital_agenda.apps.estat.importer import ImporterError
from digital_agenda.common.citext import CICharField
from digital_agenda.common.models import NaturalCodeManger


class ImportConfigTag(models.Model):
    code = CICharField(max_length=60, unique=True)

    objects = NaturalCodeManger()

    def __str__(self):
        return self.code

    def natural_key(self):
        return (self.code,)  # noqa


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
                {"size": f"Size mismatch; geo codes has {len(self.geo_codes)} codes"}
            )

    def natural_key(self):
        return (self.code,)  # noqa


def default_mappings():
    return {
        "indicator": {},
        "breakdown": {},
        "country": {"EU27_2020": "EU"},
        "unit": {},
        "period": {},
        "reference_period": {},
        "remarks": {},
    }


def default_formula():
    return {
        "formula": "",
        "symbols": {},
    }


def is_unique(values):
    return len(values) == len(set(v.lower() for v in values))


class ImportConfig(models.Model):
    class ConflictResolution(models.TextChoices):
        RAISE_ERROR = "RAISE_ERROR", "Raise errors on duplicate keys"
        SUM_VALUES = "SUM_VALUES", "Add values and merge flags"
        AVERAGE_VALUES = "AVERAGE_VALUES", "Average values and merge flags"
        USE_FORMULA = "USE_FORMULA", "Use an advanced formula to merge values"

    code = CICharField(max_length=60)
    title = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=(
            "Human readable title for logging and differentiating from multiple configs for the same dataset"
        ),
    )
    tags = models.ManyToManyField(
        ImportConfigTag,
        help_text="Assigned tags used for filtering and searching; has no impact on the data import",
        blank=True,
    )
    additional_remarks = models.TextField(
        blank=True, null=True, help_text="Additional notes/remarks"
    )

    disable_check_updates = models.BooleanField(
        default=False,
        help_text="Don't check for new data in ESTAT",
    )

    data_last_update = models.DateTimeField(
        null=True,
        help_text="Last data update of the local copy of the dataset as extracted from the ESTAT annotations",
    )
    datastructure_last_update = models.DateTimeField(
        null=True,
        help_text="Last structure update of the local copy of the dataset as extracted from the ESTAT annotations",
    )
    datastructure_last_version = models.CharField(
        null=True,
        max_length=60,
        help_text="Last version update of the local copy of the dataset as extracted from the ESTAT annotations",
    )
    new_version_available = models.BooleanField(
        default=False,
        help_text="An updated version of the dataset is available in ESTAT",
    )

    conflict_resolution = models.CharField(
        max_length=60,
        choices=ConflictResolution.choices,
        default=ConflictResolution.RAISE_ERROR,
        help_text=(
            "Importer behavior when a duplicate key is detected in the processed dataset. "
            "Can be used to merge multiple values into a single surrogate indicator."
        ),
    )
    conflict_formula = models.JSONField(
        blank=True,
        default=default_formula,
        help_text=(
            "Formula to use when conflict resolution is set to 'Use formula'. "
            "Must define both the formula and how to extract each symbol from the "
            "dataset. Each symbol may use one or multiple dimensions values to "
            "identify the corresponding observation."
        ),
    )

    value_multiplier = models.FloatField(
        default=1,
        help_text="Multiply all values by this factor before importing",
    )
    value_offset = models.FloatField(
        default=0,
        help_text="Add this value to all values before importing",
    )
    value_decimal_places = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True,
        help_text="Round all values to this number of decimal places before importing",
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

    reference_period = CICharField(
        max_length=60,
        blank=True,
        null=True,
        help_text="String only field, doesn't required related object to exist",
    )
    reference_period_is_surrogate = models.BooleanField(default=False)

    remarks = CICharField(
        max_length=60,
        blank=True,
        null=True,
        help_text="String only field, doesn't required related object to exist",
    )
    remarks_is_surrogate = models.BooleanField(default=False)

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
        help_text="Only include datapoints for countries in this group",
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
    multipliers = models.JSONField(
        default=dict,
        blank=True,
        help_text="Define multipliers to apply to specific dimensions values.",
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

        return result

    @cached_property
    def ci_mappings(self):
        result = collections.defaultdict(dict)

        for dimension, mapping in self.mappings.items():
            for original, new_value in mapping.items():
                result[dimension.lower()][original.lower()] = new_value.lower()
        return result

    @cached_property
    def ci_multipliers(self):
        result = collections.defaultdict(dict)

        for key, multipliers in self.multipliers.items():
            for dimension_value, multiplier_value in multipliers.items():
                result[key.lower()][dimension_value.lower()] = multiplier_value
        return result

    @cached_property
    def ci_formula(self):
        new_symbols = collections.defaultdict(dict)
        for symbol, definition in self.conflict_formula["symbols"].items():
            for dimension, value in definition.items():
                new_symbols[symbol][dimension.lower()] = value.lower()
        return {
            **self.conflict_formula,
            "symbols": new_symbols,
        }

    def _clean_json_dimensions(self, field_name, config_dict=None):
        if config_dict is None:
            config_dict = getattr(self, field_name)
        if not isinstance(config_dict, dict):
            raise ValidationError({field_name: "Must be a valid JSON object"})

        if not is_unique(config_dict):
            raise ValidationError({field_name: "Duplicate keys detected"})

        for key, values in config_dict.items():
            if not isinstance(values, (list, dict)):
                continue
            if not is_unique(values):
                raise ValidationError(
                    {field_name: f"Duplicate values detected for the {key!r} dimension"}
                )

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
            raise ValidationError({"period_start": error, "period_end": error})

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

        self._clean_json_dimensions("filters")
        self._clean_json_dimensions("multipliers")

        if len(self.multipliers) > 1:
            raise ValidationError(
                {"multipliers": "Only one dimension can have multipliers."}
            )

        for dimension, values in self.multipliers.items():
            for code, multiplier in values.items():
                if not isinstance(multiplier, (int, float)):
                    raise ValidationError(
                        {
                            "multipliers": f"Multiplier for {dimension!r} must be a number: {multiplier!r}"
                        }
                    )

        if self.conflict_resolution == self.ConflictResolution.USE_FORMULA:
            self._validate_formula()

    def _validate_formula(self):
        if not self.conflict_formula or not isinstance(self.conflict_formula, dict):
            raise ValidationError(
                {"conflict_formula": "Formula must be a valid JSON object"}
            )
        if set(self.conflict_formula.keys()) != {"formula", "symbols"}:
            raise ValidationError(
                {"conflict_formula": "Formula must contain formula and symbols keys"}
            )

        try:
            formula = sympify(self.conflict_formula["formula"])
        except (ValueError, KeyError) as e:
            raise ValidationError({"conflict_formula": str(e)}) from e

        defined_symbols = {symbols(key) for key in self.conflict_formula["symbols"]}
        if formula.free_symbols != defined_symbols:
            raise ValidationError(
                {
                    "conflict_formula": f"Defined symbols must match formula symbols: {formula.free_symbols} != {defined_symbols}"
                }
            )
        for symbol, symbol_definition in self.conflict_formula["symbols"].items():
            self._clean_json_dimensions("conflict_formula", symbol_definition)

    def _validate_json_dimensions(self, dataset, config_dict, config_type):
        for key, values in config_dict.items():
            if key not in dataset.dimension_ids:
                raise ImporterError(
                    {
                        f"Invalid {config_type} {key!r}, no dimensions with that id found in": dataset.dimension_ids
                    }
                )

            categories = dataset.dimension_dict[key]
            for val in values:
                if val not in categories:
                    raise ImporterError(
                        {
                            f"Invalid {config_type} value {val!r} for dimension {key!r} not found in": categories
                        }
                    )

    def clean_with_dataset(self, dataset):
        """Simple sanity checks to validate the data matches the given config."""
        self._validate_json_dimensions(dataset, self.ci_filters, "filter")
        self._validate_json_dimensions(dataset, self.ci_multipliers, "multiplier")
        for dimension in ("indicator", "breakdown", "country", "unit", "period"):
            config_dim = getattr(self, dimension)
            is_surrogate = getattr(self, f"{dimension}_is_surrogate")

            if is_surrogate:
                # No point in checking surrogates since they are hardcoded values
                continue

            if config_dim not in dataset.dimension_ids:
                raise ImporterError(
                    {
                        f"Invalid dimension {config_dim!r}, no dimensions with that id found in": dataset.dimension_ids
                    }
                )

            mappings = self.ci_mappings.get(dimension, {})
            categories = dataset.dimension_dict[config_dim]
            for val in mappings.keys():
                if val not in categories:
                    raise ImporterError(
                        {
                            f"Mapped value {val!r} for dimension {dimension!r} not found in": categories
                        }
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
        prefetched_tasks = getattr(self, "prefetched_latest_tasks", None)
        if prefetched_tasks is not None:
            try:
                return prefetched_tasks[0]
            except IndexError:
                return None

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
    dry_run = models.BooleanField(default=False)
    dry_run_report = models.FileField(
        upload_to="estat_dry_run_reports/", null=True, editable=False, default=None
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
        choices=((0, "NONE"), (1, "WARNING"), (2, "INFO"), (3, "DEBUG")),
    )
    errors = models.JSONField(null=True, blank=True)

    class Meta:
        get_latest_by = "created_on"
        verbose_name = "Import config result"
        verbose_name_plural = "Import configs results"

    @staticmethod
    def get_jobclass():
        from .jobs import ImportFromConfigJob

        return ImportFromConfigJob

    def clean(self):
        if self.dry_run and self.delete_existing:
            raise ValidationError(
                {
                    "delete_existing": "Cannot delete existing facts when running in dry-run mode"
                }
            )
