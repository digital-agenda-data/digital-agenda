import io
import itertools

import openpyxl
from django.urls import reverse
from rest_framework import status

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.models import Unit
from digital_agenda.common.test_utils import APIBaseTest


class TestDimensionAPI(APIBaseTest):
    fixtures = [
        "datasource",
        "indicatorgroup",
        "indicator",
        "indicatorgrouplink",
        "breakdowngroup",
        "breakdown",
        "breakdowngrouplink",
        "indicatordatasourcelink",
        "unit",
        "period",
        "country",
    ]

    def create_fact(
        self, indicator, breakdown, period, unit, country, value=None, flags="be"
    ):
        Fact.objects.create(
            indicator=Indicator.objects.get(code=indicator),
            breakdown=Breakdown.objects.get(code=breakdown),
            period=Period.objects.get(code=period),
            unit=Unit.objects.get(code=unit),
            country=Country.objects.get(code=country),
            value=42 if value is None else value,
            flags=flags,
        )

    def create_facts(self):
        for indicator, breakdown, period, unit, country in itertools.product(
            ["e_cc", "e_bd"],
            ["men", "women"],
            ["2020", "2021"],
            ["nr", "euro"],
            ["EU", "RO"],
        ):
            self.create_fact(indicator, breakdown, period, unit, country)

    def remove_facts(self, **kwargs):
        Fact.objects.filter(
            **{f"{key}__code": value for key, value in kwargs.items()}
        ).delete()

    def check_response_single(self, url_name, params, expected_code):
        resp = self.client.get(reverse(url_name), params)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = resp.json()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["code"], expected_code)

    def test_list_breakdown_groups(self):
        self.create_fact(
            indicator="5g_spectrum",
            breakdown="total",
            period="2020",
            unit="pc_hh",
            country="EU",
        )
        resp = self.client.get(
            reverse("v1:breakdowngroup-list") + "?indicator=5g_spectrum"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = resp.json()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["code"], "total")

    def test_list_breakdown(self):
        self.create_fact(
            indicator="5g_spectrum",
            breakdown="total",
            period="2020",
            unit="pc_hh",
            country="EU",
        )
        resp = self.client.get(reverse("v1:breakdown-list") + "?indicator=5g_spectrum")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = resp.json()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["code"], "total")

    def test_list_breakdown_with_multiple_groups(self):
        self.create_fact(
            indicator="e_ispdfokx_ge100",
            breakdown="ent_l_xfin",
            period="2020",
            unit="pc_ent",
            country="EU",
        )
        resp = self.client.get(
            reverse("v1:breakdown-list")
            + "?indicator=e_ispdfokx_ge100&breakdown_group=byentsize"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        result = resp.json()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["code"], "ent_l_xfin")

    def test_list_indicator_filter_existing_facts(self):
        self.create_facts()
        self.remove_facts(period="2021", breakdown="men", indicator="e_bd")
        self.check_response_single(
            "v1:indicator-list",
            {"period": "2021", "breakdown": "men"},
            "e_cc",
        )

    def test_list_breakdown_filter_existing_facts(self):
        self.create_facts()
        self.remove_facts(period="2021", breakdown="men", country="RO")
        self.check_response_single(
            "v1:breakdown-list",
            {"period": "2021", "country": "RO"},
            "women",
        )

    def test_list_period_filter_existing_facts(self):
        self.create_facts()
        self.remove_facts(period="2021", breakdown="men", country="RO")
        self.check_response_single(
            "v1:period-list",
            {"breakdown": "men", "country": "RO"},
            "2020",
        )

    def test_list_unit_filter_existing_facts(self):
        self.create_facts()
        self.remove_facts(period="2021", breakdown="men", unit="euro")
        self.check_response_single(
            "v1:unit-list",
            {"period": "2021", "breakdown": "men"},
            "nr",
        )

    def test_list_country_filter_existing_facts(self):
        self.create_facts()
        self.remove_facts(period="2021", breakdown="men", country="RO")
        self.check_response_single(
            "v1:country-list",
            {"period": "2021", "breakdown": "men"},
            "EU",
        )

    def get_xlsx(self, params) -> openpyxl.Workbook:
        self.create_facts()

        resp = self.client.get(
            reverse("v1:fact-list"),
            {
                **params,
                "format": "xlsx",
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        return openpyxl.load_workbook(io.BytesIO(resp.content), read_only=True)

    def check_xlsx(self, sheet_name, params, expected):
        sheet = self.get_xlsx(params)[sheet_name]

        result = {pos: sheet[pos].value for pos in expected}
        self.assertEqual(result, expected)

    def test_export_filters(self):
        self.check_xlsx(
            "Applied Filters",
            {
                "indicator": "e_cc",
                "breakdown": "women",
                "unit": "euro",
            },
            {
                "A2": "Indicator",
                "A3": "Breakdown",
                "A4": "Unit",
                "B2": "e_cc",
                "B3": "women",
                "B4": "euro",
            },
        )

    def test_export_period(self):
        self.check_xlsx(
            "Period",
            {
                "indicator": "e_cc",
                "breakdown": "women",
                "unit": "euro",
                "format": "xlsx",
            },
            {
                "A2": "2021",
                "A3": "2020",
            },
        )

    def test_export_country(self):
        self.check_xlsx(
            "Country",
            {
                "indicator": "e_cc",
                "breakdown": "women",
                "unit": "euro",
            },
            {
                "A2": "EU",
                "A3": "RO",
                "B2": "European Union",
                "B3": "Romania",
            },
        )

    def test_export_flags(self):
        self.check_xlsx(
            "Flags",
            {
                "indicator": "e_cc",
                "breakdown": "women",
                "unit": "euro",
            },
            {
                "A2": "b",
                "A3": "c",
                "A4": "d",
                "B2": "break in time series",
                "B3": "confidential",
                "B4": "definition differs, see metadata",
            },
        )

    def test_export_raw_data(self):
        self.check_xlsx(
            "Raw Data",
            {
                "indicator": "e_cc",
                "breakdown": "women",
                "period": "2021",
                "unit": "euro",
            },
            {
                "A2": "2021",
                "B2": "EU",
                "C2": "e_cc",
                "D2": "women",
                "E2": "euro",
                "F2": 42,
                "G2": "be",
                "A3": "2021",
                "B3": "RO",
                "C3": "e_cc",
                "D3": "women",
                "E3": "euro",
                "F3": 42,
                "G3": "be",
            },
        )

    def test_export_data(self):
        self.check_xlsx(
            "Data",
            {
                "indicator": "e_cc",
                "breakdown": "women",
                "period": "2021",
                "unit": "euro",
            },
            {
                "A2": "Year: 2021",
                "B2": "European Union",
                "C2": "Buy Cloud Computing services used over the internet",
                "D2": "Women",
                "E2": "Euro",
                "F2": 42,
                "G2": "break in time series, estimated",
                "A3": "Year: 2021",
                "B3": "Romania",
                "C3": "Buy Cloud Computing services used over the internet",
                "D3": "Women",
                "E3": "Euro",
                "F3": 42,
                "G3": "break in time series, estimated",
            },
        )
