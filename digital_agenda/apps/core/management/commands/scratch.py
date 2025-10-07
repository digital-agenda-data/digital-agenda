import io
import logging
import random
from pprint import pprint

import openpyxl
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import UploadedFile
from django.core.management import BaseCommand

from digital_agenda.apps.accounts.models import User
from digital_agenda.apps.core.formats import XLSXLoader
from digital_agenda.apps.core.jobs import ImportFromDataFileJob
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import DataFileImport
from digital_agenda.apps.core.models import Fact

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()
        fp = (
            settings.BASE_DIR
            / "frontend"
            / "cypress"
            / "fixtures"
            / "import_file_valid.xls"
        )
        fo = io.BytesIO(fp.open("rb").read())
        obj = DataFileImport.objects.create(
            file=File(fo, name="import_file_valid.xls"),
            user=user,
        )
        obj.run_import()
        assert obj.facts.count() == 1
        fact = obj.facts.first()
        pprint(fact.__dict__)

        # fact = Fact.objects.get(
        #     period__code="2022",
        #     country__code="EU",
        #     indicator__code="e_eturn",
        #     breakdown__code="ent_all_xfin",
        #     unit__code="pc_turn",
        # )
        # print("Remarks before: ", fact.remarks)
        #
        # Fact.objects.bulk_create(
        #     [
        #         Fact(
        #             period=fact.period,
        #             country=fact.country,
        #             indicator=fact.indicator,
        #             breakdown=fact.breakdown,
        #             unit=fact.unit,
        #             value=17.6,
        #             flags="",
        #             reference_period="2020",
        #             remarks="XXXXXXXX",
        #         )
        #     ],
        #     update_conflicts=True,
        #     update_fields=(
        #         "value",
        #         "flags",
        #         "import_file",
        #         "reference_period",
        #         "remarks",
        #     ),
        #     unique_fields=(
        #         "indicator",
        #         "breakdown",
        #         "unit",
        #         "country",
        #         "period",
        #     ),
        # )
        #
        # fact.refresh_from_db()
        # print("Remarks after: ", fact.remarks)
