import csv
import io
import json
from functools import cached_property

import httpx
import topojson
from django.conf import settings
from django.core.management import BaseCommand

from digital_agenda.common.console import console

BASE = "https://gisco-services.ec.europa.eu/distribution/v2"

EU_COUNTRIES = {
    "AT",
    "BE",
    "BG",
    "CY",
    "CZ",
    "DE",
    "DK",
    "EE",
    "EL",
    "ES",
    "FI",
    "FR",
    "HR",
    "HU",
    "IE",
    "IT",
    "LT",
    "LU",
    "LV",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SE",
    "SI",
    "SK",
}

EXTRA_COUNTRIES = {
    # "RU",
    # "UA",
}


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = ()

    @staticmethod
    def handle_response(response):
        console.print(
            f"Request '{response.url}' finished: status={response.status_code}"
        )
        response.raise_for_status()

    @cached_property
    def client(self):
        return httpx.Client(event_hooks={"response": [self.handle_response]})

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--projection",
            help="4-digit EPSG code",
            default="3857",
            choices=["4326", "3035", "3857"],
        )
        parser.add_argument(
            "-r",
            "--resolution",
            help="map scale the data is optimized for",
            default="10M",
            choices=["60M", "20M", "10M", "03M", "01M"],
        )

    def get_latest_year(self, dataset):
        resp = self.client.get(f"{BASE}/{dataset}/datasets.json").json()

        years = list(int(key.rsplit("-")[-1]) for key in resp.keys())
        years.sort(reverse=True)

        return years[0]

    def handle(self, *, projection, resolution, **options):
        nuts_year = self.get_latest_year("nuts")
        countries_year = self.get_latest_year("countries")

        nuts_countries = set()
        nuts_csv = self.client.get(f"{BASE}/nuts/csv/NUTS_AT_{nuts_year}.csv")
        for row in csv.DictReader(io.StringIO(nuts_csv.text)):
            nuts_countries.add(row["CNTR_CODE"])

        name = f"CNTR_RG_{resolution}_{countries_year}_{projection}"
        data = self.client.get(f"{BASE}/countries/topojson/{name}.json").json()
        data = topojson.Topology(data, object_name=name)

        geojson = json.loads(data.to_geojson())

        new_features = []
        for feature in geojson["features"]:
            code = feature["properties"]["CNTR_ID"]

            if code in nuts_countries or code in EXTRA_COUNTRIES:
                new_features.append(feature)
        geojson["features"] = new_features

        topofile = settings.BASE_DIR / "frontend" / "src" / "assets" / "topology.json"
        topojson.Topology(geojson).to_json(topofile)

        # with topofile.open("w") as f:
        #     topojson = topology.Topology()({"object_name": geojson}, 9)
        #     json.dump(topojson, f)
        console.print(f"New topology file written to '{topofile}'")
