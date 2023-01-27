import csv
import os.path
import shutil
import tempfile

import httpx
from django.core.management import BaseCommand

from digital_agenda.apps.core.models import *

OLD_DATA = [
    "https://digital-agenda-data.eu/download/DESI.csv.zip",
    "https://digital-agenda-data.eu/download/digital-agenda-scoreboard-key-indicators.csv.zip",
    "https://digital-agenda-data.eu/download/e-gov.csv.zip",
    "https://digital-agenda-data.eu/download/e-gov-2020.csv.zip",
]


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = ()

    def extract_flag(self, row):
        if not row["flag"]:
            return ""

        flags = [
            f.strip()[0]
            for f in row["flag"].split("#")[-1].replace("+", " ").split("%2C")
        ]
        return "".join(flags)

    def by_code(self, model):
        return {item.code: item for item in model.objects.all()}

    def handle(self, *args, **options):
        units = self.by_code(Unit)
        periods = self.by_code(Period)
        countries = self.by_code(Country)
        indicators = self.by_code(Indicator)
        breakdowns = self.by_code(Breakdown)

        with tempfile.TemporaryDirectory() as tmpdirname:
            for old in OLD_DATA:
                print(f"Processing '{old}'")

                fn = os.path.join(tmpdirname, old.split("/")[-1])

                with open(fn, "wb") as f:
                    resp = httpx.get(old)
                    resp.raise_for_status()
                    f.write(resp.content)

                shutil.unpack_archive(fn, tmpdirname, "zip")
                new_fn = os.path.join(tmpdirname, old.split("/")[-1].rsplit(".", 1)[0])

                facts = []

                # "observation","time_period","ref_area","indicator","breakdown","unit_measure","value","flag","note"
                for row in csv.DictReader(open(new_fn)):

                    x = {
                        "observation": "http://semantic.digital-agenda-data.eu/data/DESI/desi_c_mbb/desi_4g/pc_desi_c_mbb/LV/2017",
                        "time_period": "2017",
                        "ref_area": "LV",
                        "indicator": "desi_c_mbb",
                        "breakdown": "",
                        "unit_measure": "pc_desi_c_mbb",
                        "value": "0.170326",
                        "flag": "",
                        "note": "",
                    }

                    try:
                        (
                            _,
                            indicator_code,
                            breakdown_code,
                            unit_code,
                            country_code,
                            period_code,
                        ) = row["observation"].rsplit("/", 5)

                        unit = units[row["unit_measure"] or unit_code]
                        period = periods[row["time_period"] or period_code]
                        country = countries[row["ref_area"] or country_code]
                        indicator = indicators[row["indicator"] or indicator_code]
                        breakdown = breakdowns[row["breakdown"] or breakdown_code]
                    except KeyError as e:
                        print(f"Missing value {row}: {e}")
                        continue

                    value = row["value"] or None

                    if value is not None:
                        try:
                            value = float(value)
                            if 0 < value <= 1:
                                value = value * 100
                        except ValueError:
                            value = None

                    flags = self.extract_flag(row)

                    if value is None and not flags:
                        # No point in storing this info
                        continue

                    facts.append(
                        Fact(
                            period=period,
                            country=country,
                            indicator=indicator,
                            breakdown=breakdown,
                            unit=unit,
                            value=value,
                            flags=flags,
                        )
                    )

                objs = Fact.objects.bulk_create(
                    facts, ignore_conflicts=True, batch_size=10_000
                )
                print("Fact objs created", len(objs))
