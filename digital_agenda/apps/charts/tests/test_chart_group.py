from django.urls import reverse

from digital_agenda.apps.charts.models import ChartGroup
from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import IndicatorGroup
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.models import Unit
from digital_agenda.common.test_utils import APIBaseTest


class TestChartGroupTimeCoverage(APIBaseTest):
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

    def setUp(self):
        self.indicator_group = IndicatorGroup.objects.get(code="broadband")
        self.indicator = Indicator.objects.get(code="bb_dsl")
        self.breakdown = Breakdown.objects.get(code="total_fbb")
        self.country = Country.objects.get(code="EU")
        self.unit = Unit.objects.get(code="pc_lines")

        self.chart_group = ChartGroup.objects.create(
            code="test-group", name="Test Group", short_name="Test Group"
        )
        self.chart_group.indicator_groups.add(self.indicator_group)

        self.url = reverse("v1:chart-groups-indicators", args=(self.chart_group.code,))

    def check_url(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        return resp.json()

    def check_time_coverage(self, expected_coverage):
        data = self.check_url()
        self.assertEqual(len(data), 1)

        indicator = data[0]
        self.assertEqual(indicator["code"], self.indicator.code)
        self.assertEqual(indicator["time_coverage"], expected_coverage)

    def create_fact(self, period_code, reference_period=None):
        period = Period.objects.get(code=period_code)
        return Fact.objects.create(
            indicator=self.indicator,
            breakdown=self.breakdown,
            country=self.country,
            unit=self.unit,
            period=period,
            value=50,
            reference_period=reference_period,
        )

    def create_facts(self, period_codes):
        result = []
        for code in period_codes:
            result.append(self.create_fact(code))
        return result

    def test_single_period(self):
        self.create_facts(["2020"])
        self.check_time_coverage("2020")

    def test_period_range(self):
        self.create_facts(range(2020, 2023))
        self.check_time_coverage("2020-2022")

    def test_period_range_interrupted(self):
        self.create_facts(["2020", "2023", "2025"])
        self.check_time_coverage("2020, 2023, 2025")

    def test_period_multiple_ranges(self):
        self.create_facts(["2020", "2021", "2022", "2024", "2025"])
        self.check_time_coverage("2020-2022, 2024-2025")

    def test_filter_start(self):
        self.chart_group.period_start = "2023"
        self.chart_group.save()

        self.create_facts(range(2020, 2026))
        self.check_time_coverage("2023-2025")

    def test_filter_end(self):
        self.chart_group.period_end = "2023"
        self.chart_group.save()

        self.create_facts(range(2020, 2026))
        self.check_time_coverage("2020-2023")

    def test_filter_both(self):
        self.chart_group.period_start = "2022"
        self.chart_group.period_end = "2024"
        self.chart_group.save()

        self.create_facts(range(2020, 2026))
        self.check_time_coverage("2022-2024")

    def test_reference_period(self):
        self.create_fact(2023, reference_period=2018)
        self.create_fact(2024, reference_period=2019)
        self.create_fact(2025, reference_period=2020)

        self.check_time_coverage("2018-2020")

    def test_mixed_reference_period(self):
        self.create_fact(2023, reference_period=2018)
        self.create_fact(2024, reference_period=2019)
        self.create_fact(2025)

        self.check_time_coverage("2018-2019, 2025")

    def test_reference_period_filter(self):
        self.chart_group.period_start = "2022"
        self.chart_group.period_end = "2024"
        self.chart_group.save()

        self.create_fact(2021, reference_period=2016)
        self.create_fact(2022, reference_period=2017)
        self.create_fact(2023, reference_period=2018)
        self.create_fact(2024, reference_period=2019)
        self.create_fact(2025, reference_period=2020)

        self.check_time_coverage("2017-2019")

    def test_reference_period_filter_partial_match(self):
        self.chart_group.period_start = "2022"
        self.chart_group.period_end = "2024"
        self.chart_group.save()

        self.create_fact(2021, reference_period=2020)
        self.create_fact(2022, reference_period=2021)
        self.create_fact(2023, reference_period=2022)
        self.create_fact(2024, reference_period=2023)
        self.create_fact(2025, reference_period=2024)

        self.check_time_coverage("2021-2023")
