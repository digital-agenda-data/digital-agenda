import sys

from django.core.management import BaseCommand

from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.estat.models import ImportConfig


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
            "--dry-run",
            action="store_true",
            default=False,
            help="Dry run only",
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
        dry_run=False,
        noinput=False,
        **options,
    ):
        config_qs = ImportConfig.objects.all()
        if code:
            config_qs = config_qs.filter(code=code)

        if not config_qs.exists():
            print("No import configurations found", file=sys.stderr)
            sys.exit(1)

        if not noinput and delete_existing:
            nr_facts = Fact.objects.filter(import_config__in=config_qs).count()
            print(
                f"Warning! This will remove {nr_facts} facts "
                f"from {len(config_qs)} import configurations. Continue?",
                end=" ",
            )
            if input("[Y/n] ") != "Y":
                sys.exit(1)

        for config in config_qs:
            config.run_import(
                force_download=force_download,
                delete_existing=delete_existing,
                dry_run=dry_run,
            )

        if not all(config.latest_task.status == "SUCCESS" for config in config_qs):
            print("Not ALL tasks completed successfully.")
            sys.exit(1)
