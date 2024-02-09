import itertools

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

    def create_fact(self, indicator, breakdown, period, unit, country, value=None):
        Fact.objects.create(
            indicator=Indicator.objects.get(code=indicator),
            breakdown=Breakdown.objects.get(code=breakdown),
            period=Period.objects.get(code=period),
            unit=Unit.objects.get(code=unit),
            country=Country.objects.get(code=country),
            value=42 if value is None else value,
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
