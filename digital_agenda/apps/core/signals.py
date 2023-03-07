import logging
from contextlib import suppress

from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .cache import clear_all_caches
from .models import DataFileImport


logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], dispatch_uid="auto_clear_cache_receiver")
def auto_clear_cache(sender, instance=None, **kwargs):
    if getattr(sender._meta.app_config, "auto_clear_cache", False):
        clear_all_caches()


@receiver(post_save, sender=DataFileImport)
def trigger_data_import(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(  # Avoid race condition where db record is not yet created
            lambda: instance.queue_import()
        )


@receiver(post_delete, sender=DataFileImport)
def delete_data_import_file(sender, instance, using, **kwargs):
    with suppress(FileNotFoundError):
        default_storage.delete(instance.file.path)
