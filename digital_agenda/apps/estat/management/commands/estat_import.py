from django.core.management import BaseCommand

from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.estat.models import ImportConfig
from digital_agenda.apps.estat import tasks


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--code",
            help="Filter import configuration by this code",
        )
        parser.add_argument(
            "-f",
            "--force-download",
            action="store_true",
            default=False,
            help="Force re-download of the data files",
        )
        parser.add_argument(
            "-D",
            "--delete-existing",
            action="store_true",
            default=False,
            help="Delete existing facts before importing new ones",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            help="Do not prompt for any user input",
            default=False,
        )

    def handle(
        self,
        *args,
        code=None,
        force_download=False,
        delete_existing=False,
        noinput=False,
        **options,
    ):
        qs = ImportConfig.objects.all()
        if code:
            qs = qs.filter(code=code)
        ids = qs.values_list("id", flat=True)

        if not noinput and delete_existing:
            nr_facts = Fact.objects.filter(import_config_id__in=ids).count()
            print(
                f"Warning! This will remove {nr_facts} facts "
                f"from {len(ids)} import configurations. Continue?",
                end=" ",
            )
            if input("[Y/n] ") != "Y":
                return

        for config_id in ids:
            tasks.import_from_config(
                config_pk=config_id,
                force_download=force_download,
                delete_existing=delete_existing,
            )
