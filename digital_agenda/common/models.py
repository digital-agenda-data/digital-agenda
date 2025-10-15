from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DisplayOrderModel(models.Model):
    display_order = models.PositiveIntegerField(default=100_000, db_index=True)

    class Meta:
        abstract = True


class NaturalCodeManger(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class CleanCKEditor5Field(CKEditor5Field):
    """
    CKEditor5 field that automatically cleans empty <p></p> content.
    """

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return ""
        # Strip whitespace and check for empty CKEditor output
        stripped = value.strip()
        if stripped in ("<p></p>", "<p>&nbsp;</p>", "<p> </p>", "<p> </p>"):
            return ""
        return value
