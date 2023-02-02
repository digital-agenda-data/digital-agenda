import sys

from django.conf import settings
from django.core.files import File
from django.core.management import BaseCommand
from django.core.management import call_command

from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.cache import clear_all_caches


class Command(BaseCommand):
    help = "Seed DB for E2E tests"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            help="Do not prompt for any user input",
            default=False,
        )

    def handle(self, *args, noinput=False, **options):
        if not noinput:
            print(
                "This will IRREVERSIBLY DESTROY all data currently in the  database! "
                "Are you sure you want to continue?",
                end=" ",
            )
            if input("[Y/n] ") != "Y":
                sys.exit(1)

        call_command("flush", "--noinput")
        call_command("load_initial_fixtures", "--test", "--exclude", "importconfigs")

        # Import some facts from some small configs
        call_command("loaddata", "test/seed_importconfigs")
        call_command("estat_import")

        dir_path = (
            settings.BASE_DIR
            / "digital_agenda"
            / "apps"
            / "charts"
            / "fixtures"
            / "test"
        )
        for group in ChartGroup.objects.all():
            img_path = dir_path / f"{group.code}.png"
            with img_path.open("rb") as f:
                group.image = File(f, name=img_path.name)
                group.save()

        clear_all_caches(force=True)
