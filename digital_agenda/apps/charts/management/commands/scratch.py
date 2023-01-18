import collections
import csv
import itertools
import json
import os
from pprint import pprint

import requests
import django.db
import django.core.exceptions
from django.conf import settings
from django.core.management import BaseCommand
from pandasdmx.reader import READERS
from pandasdmx.reader import sdmxml

from digital_agenda.apps.charts.models import *
from digital_agenda.apps.core.models import *
from digital_agenda.common.console import console

MAP = {
    "desi": {
        "desi-composite.json": "1-desi-composite-index",
        "desi-components.json": "1-desi-by-components",
        "desi-see-the-evolution-of-an-indicator-and-compare-breakdowns.json": "1-compare-the-evolution-of-desi-components",
        "desi-see-the-evolution-of-two-indicators-and-compare-countries.json": "1-desi-compare-countries-progress",
        "desi-compare-two-indicators.json": "1-desi-compare-two-indicators",
    },
    "key-indicators": {
        "analyse-one-indicator-and-compare-countries.json": "2-analyse-one-indicator-and-compare-countries",
        "analyse-one-indicator-and-compare-breakdowns.json": "2-analyse-one-indicator-and-compare-breakdowns",
        "see-the-evolution-of-an-indicator-and-compare-countries.json": "2-see-the-evolution-of-an-indicator-and-compare-co",
        "see-the-evolution-of-an-indicator-and-compare-breakdowns.json": "2-see-the-evolution-of-an-indicator-and-compare-br",
        "country-profiles-the-relative-position-against-all-other-european-countries.json": "2-country-profiles-the-relative-position-against-a",
        "country-ranking-table-on-a-thematic-group-of-indicators.json": "2-country-ranking-table-on-a-thematic-group-of-ind",
        "maps-by-country.json": "2-maps-by-country",
        "compare-two-indicators.json": "2-compare-two-indicators",
        "compare-two-indicators-using-country-bubbles-sized-on-a-third-one.json": "2-compare-two-indicators-using-country-bubbles-siz",
        "compare-the-evolution-of-two-indicators.json": "2-compare-the-evolution-of-two-indicators",
    },
    "e-gov-2020": {
        "copy_of_e-gov-analyse-one-indicator-and-compare-countries.json": "3-analyse-one-indicator-and-compare-countries",
        "copy_of_e-gov-analyse-one-indicator-and-compare-breakdowns.json": "3-analyse-one-indicator-by-life-events",
        "copy_of_e-gov-see-the-evolution-of-an-indicator-and-compare-countries.json": "3-see-the-evolution-of-an-indicator-and-compare-co",
        "copy_of_e-gov-see-the-evolution-of-an-indicator-and-compare-breakdowns.json": "3-see-the-evolution-of-an-indicator-by-life-events",
        "copy_of_e-gov-maps-by-country.json": "3-maps-by-country",
        "copy_of_e-gov-compare-two-indicators.json": "3-compare-two-indicators",
        "copy_of_e-gov-compare-two-indicators-using-country-bubbles-sized-on-a-third-one.json": "3-compare-two-indicators-using-country-bubbles-siz",
        "copy_of_e-gov-compare-the-evolution-of-two-indicators.json": "3-compare-the-evolution-of-two-indicators",
    },
    "e-gov": {
        "e-gov-analyse-one-indicator-and-compare-countries.json": "4-analyse-one-indicator-and-compare-countries",
        "e-gov-analyse-one-indicator-and-compare-breakdowns.json": "4-analyse-one-indicator-by-life-events",
        "e-gov-see-the-evolution-of-an-indicator-and-compare-countries.json": "4-see-the-evolution-of-an-indicator-and-compare-co",
        "e-gov-see-the-evolution-of-an-indicator-and-compare-breakdowns.json": "4-see-the-evolution-of-an-indicator-by-life-events",
        "e-gov-maps-by-country.json": "4-maps-by-country",
        "e-gov-compare-two-indicators.json": "4-compare-two-indicators",
        "e-gov-compare-two-indicators-using-country-bubbles-sized-on-a-third-one.json": "4-compare-two-indicators-using-country-bubbles-siz",
        "e-gov-compare-the-evolution-of-two-indicators.json": "4-compare-the-evolution-of-two-indicators",
    },
}

CONVERT = {
    "indicator-group": "indicator_group",
    "indicator": "indicator",
    "breakdown-group": "breakdown_group",
    "breakdown": "breakdown",
    "unit-measure": "unit",
    "ref-area": "country",
}

OLD_DATA = [
    settings.BASE_DIR / ".fs" / "old-data" / "desi.csv",
    settings.BASE_DIR / ".fs" / "old-data" / "key-indicators.csv",
    settings.BASE_DIR / ".fs" / "old-data" / "e-gov-2020.csv",
    settings.BASE_DIR / ".fs" / "old-data" / "e-gov.csv",
]


class CustomReader(sdmxml.Reader):
    content_types = sdmxml.Reader.content_types + [
        "application/vnd.sdmx.generic+xml;version=2.1"
    ]




class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = ()

    def handle(self, *args, **options):
        import psutil
        proc = psutil.Process()

        start = proc.memory_info().rss

        with open(".fs/estat/isoc_ec_ibuy.json") as f:
            x = json.load(f)

        end = proc.memory_info().rss
        print("Memory increase", (end - start) / 10 ** 6, "MB")

        # https://ec.europa.eu/eurostat/databrowser/view/isoc_ci_eu_en2/default/table?lang=en
        # https://ec.europa.eu/eurostat/databrowser/view/avia_tf_aca/default/table?lang=en


        # import sdmx
        #
        # # READERS.append(CustomReader)
        #
        # # https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/datastructure/ESTAT/educ_uoe_grad03/latest?references=descendants&compressed=true
        # # code = "educ_uoe_grad03"
        # # code = "isoc_ci_eu_en2"
        # # url = (
        # #     f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/datastructure/ESTAT/{code}/latest"
        # #   f"?references=descendants"
        # # )
        # # https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/datastructure/ESTAT/educ_uoe_grad03/latest
        #
        # # https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_grad03
        #
        # # with open(".fs/bulk_downloads/educ_uoe_grad03.dsd.xml", "rb") as f:
        # # with open(f"/home/kiro/Downloads/ESTAT_EDUC_UOE_GRAD03_1.0.xml", "rb") as f:
        # #     dsd = sdmx.read_sdmx(f)
        # # estat = sdmx.Client("ESTAT")
        # # estat.get
        # # dsd = estat.datastructure(code)
        #
        # ids = [
        #     "freq",
        #     "unit",
        #     "isced11",
        #     "iscedf13",
        #     "sex",
        #     "geo",
        #     "TIME_PERIOD",
        # ]
        #
        # with open(".fs/bulk_downloads/estat_educ_uoe_grad03_en.json", "r") as f:
        #     json_stat = JSONStat(f)
        #     json_values = {
        #         tuple(cat.id for cat in categories): value
        #         for categories, value in json_stat
        #     }
        #
        # import ipdb
        #
        # ipdb.set_trace()
        # pass
        #
        # with open(".fs/bulk_downloads/estat_educ_uoe_grad03_en.csv", "r") as f:
        #     for row in csv.DictReader(f):
        #         value = row["OBS_VALUE"]
        #         if value == "":
        #             value = None
        #
        #         try:
        #             value = float(value)
        #         except (ValueError, TypeError):
        #             pass
        #
        #         status = row["OBS_FLAG"] or None
        #
        #         key = tuple(row[i] for i in ids)
        #         try:
        #             datapoint = json_values[key]
        #             assert (
        #                 datapoint.value == value and datapoint.status == status
        #             ), f"Incorrect value for key {key}: {datapoint, value, status}"
        #         except Exception as e:
        #             import ipdb
        #
        #             ipdb.set_trace()
        #             raise
        #         else:
        #             print(key, "Valid")
        #
        # # from pyjstat import pyjstat
        # # with open(".fs/bulk_downloads/estat_educ_uoe_grad03_en.json", "r") as f:
        # #     ds = pyjstat.Dataset.read(f)
        # #
        # # import ipdb
        # # ipdb.set_trace()
        # #
        # # df = ds.write("dataframe")
        # # for index, row in enumerate(df.iterrows()):
        # #     print(row["freq"], row["value"])
        # #     if index == 10:
        # #         break
        #
        # # data = estat.data(code, params={"FREQ": "A"})
        # # print(list(data.series.keys()))
        #
        # # pprint(
        # #     list(
        # #         Indicator.objects.values_list(
        # #             "code", "label", "groups__code", "groups__chartgroup__code"
        # #         )
        # #     )
        # # )
        # # pprint(
        # #     list(
        # #         ChartGroup.objects.values_list(
        # #             "code",
        # #             "indicator_groups__code",
        # #             "indicator_groups__indicators__code",
        # #             "indicator_groups__indicators__label",
        # #         )[:]
        # #     )
        # # )
        #
        # # # for key, values in MAP.items():
        # # #     for fn, new_slug in values.items():
        # # #         if new_slug == "1-desi-composite-index":
        # # #             continue
        # # #
        # # #         print("\n")
        # # #         print("=" * 20)
        # # #         print(key, fn, new_slug)
        # # #         chart = Chart.objects.get(code=new_slug)
        # # #         conf = json.load(
        # # #             open(settings.BASE_DIR / ".fs" / "old-configs" / key / fn)
        # # #         )
        # # #
        # # #         for f in conf.get("facets", []):
        # # #             d = f.get("ignore_values")
        # # #             dim = f.get("dimension")
        # # #             if dim and d and d != ["EU"]:
        # # #                 print("\t", dim, d)
        # # #
        # # #                 if not isinstance(d, list):
        # # #                     d = [d]
        # # #                 rel = getattr(chart, f"{CONVERT[dim]}_filter_ignored")
        # # #                 rel.clear()
        # # #
        # # #                 for i in d:
        # # #                     if i not in ["ASS", "EU_AVERAGE", "EU_HARMONISED"]:
        # # #                         print(f"Adding '{i}' to '{chart}'")
        # # #                         obj = rel.model.objects.get(code=i)
        # # #                         rel.add(obj)
        # #
        # # for key, values in MAP.items():
        # #     for fn, new_slug in values.items():
        # #         print("\n")
        # #         print("=" * 20)
        # #         print(key, fn, new_slug)
        # #         chart = Chart.objects.get(code=new_slug)
        # #         conf = json.load(
        # #             open(settings.BASE_DIR / ".fs" / "old-configs" / key / fn)
        # #         )
        # #
        # #         for f in conf.get("facets", []):
        # #             d = f.get("default_value")
        # #             dim = f.get("dimension")
        # #             if (
        # #                 d
        # #                 and d != ["#random"]
        # #                 and d != "#random"
        # #                 and d != "EU"
        # #                 and d != ["EU", "#random"]
        # #                 and d != ["#random", "EU"]
        # #                 and not isinstance(d, dict)
        # #                 and not (
        # #                     dim == "breakdown"
        # #                     and isinstance(d, list)
        # #                     and "total_offers8plus" in d
        # #                 )
        # #                 and d != "total"
        # #                 # and dim == "ref-area"
        # #             ):
        # #                 print("\t", dim, d)
        # #                 # rel = getattr(chart, f"{CONVERT[dim]}_filter_defaults")
        # #                 # rel.clear()
        # #                 #
        # #                 # if not isinstance(d, list):
        # #                 #     d = [d]
        # #                 #
        # #                 # for i in d:
        # #                 #     print(f"Adding '{i}' to '{chart}'")
        # #                 #     obj = rel.model.objects.get(code=i)
        # #                 #     rel.add(obj)
