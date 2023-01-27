from datetime import datetime
from pathlib import Path

import magic
from colorfield.fields import ColorField

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import CICharField
from django.core.exceptions import ValidationError
from django.core.files.storage import get_storage_class
from django.core.validators import FileExtensionValidator
from django.utils.functional import cached_property

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
    definition = models.TextField(null=True, blank=True)

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


class DataSource(BaseDimensionModel):
    """Data sources for indicators (higher dimension, not referenced by facts"""

    url = models.URLField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "data_sources"
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
        db_table = "indicator_groups"
        ordering = ["display_order", "code"]


class Indicator(BaseDimensionModel):
    """Dimension model for indicators"""

    data_source = models.ForeignKey(
        "DataSource",
        on_delete=models.CASCADE,
        related_name="indicators",
        null=True,
        blank=True,
    )
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "indicators"
        ordering = ["code"]


class IndicatorGroupLinkManager(models.Manager):
    def get_by_natural_key(self, indicator_code, group_code):
        return self.get(indicator__code=indicator_code, group__code=group_code)


class IndicatorGroupLink(DisplayOrderModel):
    indicator = models.ForeignKey("Indicator", on_delete=models.CASCADE)
    group = models.ForeignKey("IndicatorGroup", on_delete=models.CASCADE)

    objects = IndicatorGroupLinkManager()

    class Meta:
        db_table = "indicators_groups"
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
        db_table = "breakdown_groups"
        ordering = ["display_order", "code"]


class Breakdown(BaseDimensionModel):
    """Dimension model for secondary dimensions, a.k.a. breakdowns."""

    class Meta:
        db_table = "breakdowns"
        ordering = ["code"]


class BreakdownGroupLinkManager(models.Manager):
    def get_by_natural_key(self, breakdown_code, group_code):
        return self.get(breakdown__code=breakdown_code, group__code=group_code)


class BreakdownGroupLink(DisplayOrderModel):
    breakdown = models.ForeignKey("Breakdown", on_delete=models.CASCADE)
    group = models.ForeignKey("BreakdownGroup", on_delete=models.CASCADE)

    objects = BreakdownGroupLinkManager()

    class Meta:
        db_table = "breakdowns_groups"
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
        db_table = "units"
        ordering = ["code"]


class Country(BaseDimensionModel):
    """Dimension model for countries / country group entities."""

    color = ColorField(
        help_text="Color used for this countries chart series", default="#CCCCCC"
    )
    is_group = models.BooleanField(default=False)

    class Meta:
        db_table = "countries"
        verbose_name_plural = "Countries"
        ordering = ["code"]


class Period(BaseDimensionModel):
    """Dimension model for time periods"""
    code = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = "periods"
        ordering = ["-code"]


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
    import_config = models.ForeignKey(
        "estat.ImportConfig",
        null=True,
        on_delete=models.CASCADE,
        related_name="facts",
    )

    class Meta:
        db_table = "facts"
        unique_together = ("indicator", "breakdown", "unit", "country", "period")
        constraints = [
            models.CheckConstraint(
                check=models.Q(value__isnull=False) | ~models.Q(flags=""),
                name="core_fact_either_val_or_flags",
            )
        ]

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


def _import_files_storage():
    storage_class = get_storage_class(settings.DEFAULT_STORAGE_CLASS)
    return storage_class()


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
    class ImportStatusChoices(models.TextChoices):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        SUCCESS = "success"
        FAILED = "failed"

    file = models.FileField(
        storage=_import_files_storage,
        upload_to=upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.IMPORT_FILES_ALLOWED_EXTENSIONS,
                message="File extension not supported.",
            ),
            validate_upload_mime_type,
        ],
    )
    status = models.CharField(
        max_length=20,
        choices=ImportStatusChoices.choices,
        default=ImportStatusChoices.PENDING,
    )
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    errors = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "data_file_imports"

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
