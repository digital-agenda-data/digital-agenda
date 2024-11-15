import re
import calendar
from datetime import date
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import magic
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.functional import cached_property
from django_task.models import TaskRQ

from digital_agenda.common.citext import CICharField
from digital_agenda.common.models import DisplayOrderModel
from digital_agenda.common.models import TimestampedModel


class BaseDimensionManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class BaseDimensionModel(TimestampedModel):
    """
    Base model for dimension-like models, with a unique code and label/short label fields.
    """

    code = CICharField(max_length=60, unique=True)
    label = models.TextField(null=True, blank=True)
    alt_label = models.TextField(null=True, blank=True, verbose_name="Alt. label")
    definition = RichTextField(null=True, blank=True)

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
            return str(self.code)


class DataSource(BaseDimensionModel):
    """Data sources for indicators (higher dimension, not referenced by facts"""

    url = models.URLField(null=True, blank=True)
    note = RichTextField(null=True, blank=True)

    class Meta:
        ordering = ["code"]


class IndicatorGroup(BaseDimensionModel, DisplayOrderModel):
    """
    Model for groups of indicators. Groups are not referenced directly by facts,
    and function as a hierarchical dimension table.
    """

    indicators = models.ManyToManyField(
        "Indicator", through="IndicatorGroupLink", related_name="groups", blank=True
    )

    class Meta:
        ordering = ["display_order", "code"]


class IndicatorDataSourceLinkManager(models.Manager):
    def get_by_natural_key(self, indicator_code, data_source_code):
        return self.get(
            indicator__code=indicator_code, data_source__code=data_source_code
        )


class IndicatorDataSourceLink(models.Model):
    indicator = models.ForeignKey("Indicator", on_delete=models.CASCADE)
    data_source = models.ForeignKey("DataSource", on_delete=models.CASCADE)

    objects = IndicatorDataSourceLinkManager()

    class Meta:
        unique_together = ("indicator", "data_source")

    def natural_key(self):
        return self.indicator.code, self.data_source.code


class Indicator(BaseDimensionModel):
    """Dimension model for indicators"""

    data_sources = models.ManyToManyField(
        "DataSource",
        through=IndicatorDataSourceLink,
        related_name="indicators",
        blank=True,
    )
    time_coverage = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        help_text="Time coverage to display instead of the automatically calculated one",
    )
    note = RichTextField(null=True, blank=True)

    class Meta:
        ordering = ["code"]


class IndicatorGroupLinkManager(models.Manager):
    def get_by_natural_key(self, indicator_code, group_code):
        return self.get(indicator__code=indicator_code, group__code=group_code)


class IndicatorGroupLink(DisplayOrderModel):
    indicator = models.ForeignKey("Indicator", on_delete=models.CASCADE)
    group = models.ForeignKey("IndicatorGroup", on_delete=models.CASCADE)

    objects = IndicatorGroupLinkManager()

    class Meta:
        unique_together = ("indicator", "group")
        ordering = ["display_order"]
        verbose_name = "indicator"
        verbose_name_plural = "membership"

    def __str__(self):
        return f"{self.group} -> {self.indicator}"

    def natural_key(self):
        return self.indicator.code, self.group.code


class BreakdownGroup(BaseDimensionModel, DisplayOrderModel):
    """
    Model for groups of breakdowns. Groups are not referenced directly by facts,
    and function as a hierarchical dimension table.
    """

    breakdowns = models.ManyToManyField(
        "Breakdown", through="BreakdownGroupLink", related_name="groups", blank=True
    )

    class Meta:
        ordering = ["display_order", "code"]


class Breakdown(BaseDimensionModel):
    """Dimension model for secondary dimensions, a.k.a. breakdowns."""

    class Meta:
        ordering = ["code"]


class BreakdownGroupLinkManager(models.Manager):
    def get_by_natural_key(self, breakdown_code, group_code):
        return self.get(breakdown__code=breakdown_code, group__code=group_code)


class BreakdownGroupLink(DisplayOrderModel):
    breakdown = models.ForeignKey("Breakdown", on_delete=models.CASCADE)
    group = models.ForeignKey("BreakdownGroup", on_delete=models.CASCADE)

    objects = BreakdownGroupLinkManager()

    class Meta:
        unique_together = ("breakdown", "group")
        ordering = ["display_order"]
        verbose_name = "breakdown"
        verbose_name_plural = "membership"

    def __str__(self):
        return f"{self.group} -> {self.breakdown}"

    def natural_key(self):
        return self.breakdown.code, self.group.code


class Unit(BaseDimensionModel):
    """Dimension model for measure units"""

    class Meta:
        ordering = ["code"]


class Country(BaseDimensionModel):
    """Dimension model for countries / country group entities."""

    color = ColorField(
        help_text="Color used for this countries chart series", default="#CCCCCC"
    )
    is_group = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["code"]


class Period(BaseDimensionModel):
    """Dimension model for time periods"""

    date = models.DateField(null=False, blank=True, db_index=True)

    class Meta:
        ordering = ["-code"]

    @staticmethod
    def split_code(code):
        if isinstance(code, float):
            assert int(code) == code
            year, qualifier = str(int(code)), ""
        elif isinstance(code, int):
            year, qualifier = str(code), ""
        else:
            try:
                year, qualifier = re.split(r"[-_\s]", code.lower(), maxsplit=1)
            except ValueError:
                year, qualifier = code, ""
        return year, qualifier

    def _guess_fields_from_code(self):
        assert self.code, "Code missing"
        year, qualifier = self.split_code(self.code)

        year = int(year)
        assert year >= 1900, f"year for date is likely too low '{year}'"
        assert year <= date.today().year, f"year appears to be in the future '{year}'"

        if not qualifier:
            self.label = self.label or f"Year: {year}"
            self.alt_label = self.alt_label or str(year)
        else:
            self.label = self.label or self.code.upper()
            self.alt_label = self.label or self.code.upper()

        if not qualifier:
            # Annual
            index = 1
            length = 12
        elif qualifier.startswith("h") or qualifier.startswith("s"):
            # Half-yearly, semesterly
            index = int(qualifier[1])
            length = 6
        elif qualifier.startswith("q"):
            # Quarterly
            index = int(qualifier[1])
            length = 3
        else:
            # Monthly (hopefully)
            # Strip any leading zeros from stuff like "2022-06"
            index = int(qualifier.lstrip("0"))
            length = 1

        first_month = (index - 1) * length + 1
        last_month = index * length
        last_day = calendar.monthrange(year, last_month)[1]

        date_start = date(year, first_month, 1)
        date_end = date(year, last_month, last_day)

        mid_date = date_start + timedelta(days=round((date_end - date_start).days / 2))
        self.date = self.date or mid_date

    def clean(self):
        if self.date:
            return

        try:
            self._guess_fields_from_code()
        except (ValueError, TypeError, AssertionError) as e:
            raise ValidationError(
                {
                    "date": f"Unable to guess date; please check code or enter a date manually: {e}"
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Fact(TimestampedModel):
    """
    The facts table, center of the star schema.
    """

    value = models.FloatField(null=True, blank=True)
    flags = models.CharField(max_length=12, blank=True)
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
    reference_period = CICharField(max_length=60, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    import_config = models.ForeignKey(
        "estat.ImportConfig",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="facts",
    )
    import_file = models.ForeignKey(
        "core.DataFileImport",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="facts",
    )

    class Meta:
        unique_together = ("indicator", "breakdown", "unit", "country", "period")
        constraints = [
            models.CheckConstraint(
                check=models.Q(value__isnull=False) | ~models.Q(flags=""),
                name="core_fact_either_val_or_flags",
            )
        ]


def upload_path(instance, filename):
    ts = (
        datetime.now()
        .isoformat()
        .replace("-", "")
        .replace(":", "")
        .replace("T", "")
        .split(".")[0]
    )
    filename = Path(settings.IMPORT_FILES_SUBDIR) / Path(filename).with_stem(
        f"{Path(filename).stem}_{ts}"
    )
    return filename


def validate_upload_mime_type(file):
    mime_type = magic.from_buffer(file.read(), mime=True)
    if mime_type not in settings.IMPORT_FILES_ALLOWED_MIME_TYPES:
        raise ValidationError("File type not supported.")


class DataFileImport(TimestampedModel):
    file = models.FileField(
        upload_to=upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.IMPORT_FILES_ALLOWED_EXTENSIONS,
                message="File extension not supported.",
            ),
            validate_upload_mime_type,
        ],
    )
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Upload data from file"
        verbose_name_plural = "Upload data from file"

    @property
    def path(self):
        return Path(self.file.path)

    def __str__(self):
        return self.path.name

    @property
    def file_name(self):
        return self.path.name

    @cached_property
    def mime_type(self):
        return magic.from_buffer(self.file.read(), mime=True)

    def run_import(self, **kwargs):
        return self._run_import(False, **kwargs)

    def queue_import(self, **kwargs):
        return self._run_import(True, **kwargs)

    def _run_import(self, is_async, **kwargs):
        task = DataFileImportTask.objects.create(import_file=self, **kwargs)
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
        except DataFileImportTask.DoesNotExist:
            return None


class DataFileImportTask(TaskRQ):
    DEFAULT_VERBOSITY = 2
    TASK_QUEUE = "default"
    TASK_TIMEOUT = 30 * 60
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    import_file = models.ForeignKey(
        DataFileImport, on_delete=models.CASCADE, related_name="tasks"
    )
    delete_existing = models.BooleanField(
        default=False,
        help_text="Delete facts linked to this import file before starting the import",
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
        verbose_name = "Upload file result"
        verbose_name_plural = "Upload file results"

    @staticmethod
    def get_jobclass():
        from .jobs import ImportFromDataFileJob

        return ImportFromDataFileJob


class StaticPage(TimestampedModel):
    title = models.CharField(max_length=255)
    code = models.SlugField(max_length=255, unique=True)
    body = RichTextField()
