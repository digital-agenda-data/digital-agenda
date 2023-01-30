from django.db import models


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
