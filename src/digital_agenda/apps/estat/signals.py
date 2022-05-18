from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Dataset, DatasetConfig, Dimension


@receiver(post_save, sender=Dataset)
def handle_new_dataset(sender, instance: Dataset, created, **kwargs):

    if created:
        DatasetConfig.objects.create(dataset=instance)
        Dimension.objects.create(
            dataset=instance,
            code=Dimension.SURROGATE_CODE,
            label="Surrogates dimension",
        )
