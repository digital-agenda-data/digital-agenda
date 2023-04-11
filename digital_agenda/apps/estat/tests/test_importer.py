import json

from django.conf import settings
from django.test import TestCase

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import DataSource
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.models import Unit
from digital_agenda.apps.estat.models import ImportConfig

EU27_2020 = [
    "at",
    "be",
    "bg",
    "cy",
    "cz",
    "de",
    "dk",
    "ee",
    "el",
    "es",
    "eu",
    "fi",
    "fr",
    "hr",
    "hu",
    "ie",
    "it",
    "lt",
    "lu",
    "lv",
    "mt",
    "nl",
    "pl",
    "pt",
    "ro",
    "se",
    "si",
    "sk",
]


class TestImporterSuccess(TestCase):
    config = None
    fixtures = ["geogroups", "test/importconfig.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = ImportConfig.objects.first()
        cls.config.run_import(delete_existing=True)
        cls.config.refresh_from_db()

    def test_status(self):
        self.assertEqual(self.config.latest_task.status, "SUCCESS")

    def test_fact_value(self):
        fact = Fact.objects.get(
            indicator__code="h_comp",
            breakdown__code="a1",
            unit__code="pc_hh",
            period__code="2010",
            country__code="EU",
        )
        self.assertEqual(fact.value, 58.58)

    def test_fact_flag(self):
        fact = Fact.objects.get(
            indicator__code="h_comp",
            breakdown__code="a1_dch",
            unit__code="pc_hh",
            period__code="2010",
            country__code="NL",
        )
        self.assertEqual(fact.flags, "u")

    def test_indicators(self):
        self.assertEqual(Indicator.objects.count(), 1)

        indicator = Indicator.objects.first()
        self.assertEqual(indicator.code.lower(), "h_comp")
        self.assertEqual(
            indicator.label,
            "Households having access to, via one of its members, a computer",
        )

    def test_data_source(self):
        indicator = Indicator.objects.first()

        self.assertEqual(DataSource.objects.count(), 1)
        self.assertEqual(indicator.data_sources.count(), 1)

        data_source = DataSource.objects.first()
        self.assertEqual(data_source.code.lower(), "estat_isoc_ci_cm_h")
        self.assertEqual(data_source.label, "Households - availability of computers")
        self.assertEqual(
            data_source.url,
            "https://ec.europa.eu/eurostat/web/products-datasets/-/isoc_ci_cm_h",
        )

    def test_breakdown(self):
        self.assertEqual(Breakdown.objects.count(), 2)

        breakdown1 = Breakdown.objects.get(code="a1")
        breakdown2 = Breakdown.objects.get(code="a1_dch")

        self.assertEqual(breakdown1.label, "Single person")
        self.assertEqual(breakdown2.label, "Single person with dependent children")

    def test_unit(self):
        self.assertEqual(Unit.objects.count(), 1)

        unit = Unit.objects.first()
        self.assertEqual(unit.code.lower(), "pc_hh")
        self.assertEqual(unit.label, "Percentage of households")

    def test_period(self):
        expected = [2010, 2011, 2012, 2013]
        codes = Period.objects.order_by("code").values_list("code", flat=True)
        labels = Period.objects.order_by("label").values_list("label", flat=True)

        self.assertEqual(expected, list(codes))
        self.assertEqual(expected, list(map(int, labels)))

    def test_country(self):
        codes = Country.objects.order_by("code").values_list("code", flat=True)

        # It's actually 28 because we expect "EU" as well
        self.assertEqual(len(codes), 28)
        self.assertEqual(EU27_2020, list(codes))


class TestImporter(TestCase):
    fixtures = ["geogroups", "test/importconfig.json"]

    def test_download(self):
        config = ImportConfig.objects.first()
        config.run_import(delete_existing=True, force_download=True)

        expected_path = settings.ESTAT_DOWNLOAD_DIR / f"{config.code}.json"
        self.assertTrue(expected_path.is_file())

    def test_download_invalidate_cache(self):
        config = ImportConfig.objects.first()
        config.run_import(delete_existing=True, force_download=True)

        expected_path = settings.ESTAT_DOWNLOAD_DIR / f"{config.code}.json"
        self.assertTrue(expected_path.is_file())

        with expected_path.open("r") as f:
            dataset = json.load(f)
            original_version = dataset["extension"]["datastructure"]["version"]
            dataset["extension"]["datastructure"]["version"] = "Hornet"

        with expected_path.open("w") as f:
            json.dump(dataset, f)

        config = ImportConfig.objects.first()
        config.run_import()

        with expected_path.open("r") as f:
            dataset = json.load(f)
            self.assertEqual(
                original_version, dataset["extension"]["datastructure"]["version"]
            )

    def test_surrogate_indicator(self):
        config = ImportConfig.objects.first()
        config.indicator = "jingle_jangle"
        config.indicator_is_surrogate = True
        config.save()

        config.run_import(delete_existing=True)

        expected = ["jingle_jangle"]
        codes = Indicator.objects.values_list("code", flat=True)
        fact_codes = Fact.objects.values_list("indicator__code", flat=True).distinct()

        self.assertEqual(expected, list(codes))
        self.assertEqual(expected, list(fact_codes))

    def test_delete_existing(self):
        config = ImportConfig.objects.first()
        config.run_import(delete_existing=True)

        # Change the filter to check that old data has been removed
        config.filters = {"hhtyp": ["A2"]}
        config.save()

        config.run_import(delete_existing=True)

        breakdown_codes = Fact.objects.values_list(
            "breakdown__code", flat=True
        ).distinct()
        self.assertEqual(["a2"], list(breakdown_codes))

        # The old breakdowns should not be removed, only the facts
        breakdowns = Breakdown.objects.order_by("code").values_list("code", flat=True)
        self.assertEqual(["a1", "a1_dch", "a2"], list(breakdowns))

    def test_keep_existing(self):
        config = ImportConfig.objects.first()
        config.run_import(delete_existing=True)

        # Change the filter to check that old data has been removed
        config.filters = {"hhtyp": ["A2"]}
        config.save()

        config.run_import()

        breakdown_codes = (
            Fact.objects.order_by("breakdown__code")
            .values_list("breakdown__code", flat=True)
            .distinct()
        )
        self.assertEqual(["a1", "a1_dch", "a2"], list(breakdown_codes))

    def test_update_existing(self):
        config = ImportConfig.objects.first()
        config.run_import(delete_existing=True)
        original_fact = Fact.objects.first()

        new_fact = Fact.objects.get(pk=original_fact.pk)
        new_fact.value = (original_fact.value or 0) + 100
        new_fact.flags = (original_fact.flags or "") + "XX"
        new_fact.import_config = None
        new_fact.save()

        config.run_import()
        new_fact.refresh_from_db()
        self.assertEqual(new_fact.value, original_fact.value)
        self.assertEqual(new_fact.flags, original_fact.flags)
        self.assertEqual(new_fact.import_config, original_fact.import_config)


class TestImporterErrors(TestCase):
    fixtures = ["geogroups", "test/importconfig.json"]

    def setUp(self):
        super().setUp()
        self.config = ImportConfig.objects.first()

    def check_error(self, msg):
        self.config.save()
        self.config.run_import(delete_existing=True)
        self.config.refresh_from_db()
        self.assertIn(msg, self.config.latest_task.failure_reason)

    def test_invalid_filter(self):
        self.config.filters = ["EU"]
        self.check_error("Must be a valid JSON object")

    def test_invalid_filter_key(self):
        self.config.filters = {"geoX": ["EU"]}
        self.check_error("no dimensions with that id found")

    def test_invalid_filter_key_duplicate(self):
        self.config.filters = {"geo": ["EU"], "GEO": ["EU"]}
        self.check_error("Duplicate keys detected")

    def test_invalid_filter_value(self):
        self.config.filters = {"geo": ["EUROVISION"]}
        self.check_error("for dimension 'geo' not found")

    def test_invalid_filter_value_duplicate(self):
        self.config.filters = {"geo": ["EU", "eu"]}
        self.check_error("Duplicate values detected")

    def test_invalid_dimension_indicator(self):
        self.config.indicator = "mrhouse"
        self.check_error("no dimensions with that id found")

    def test_invalid_mapping(self):
        self.config.mappings = []
        self.check_error("Must be a valid JSON object")

    def test_invalid_mapping_type(self):
        self.config.mappings = {"country": []}
        self.check_error("Must be a valid JSON object")

    def test_invalid_mapping_key(self):
        self.config.mappings = {"countryX": {"EU27_2020": "EU"}}
        self.check_error("Invalid mappings")

    def test_invalid_mapping_key_duplicate(self):
        self.config.mappings = {
            "country": {"EU27_2020": "EU"},
            "CountrY": {"EU27_2020": "EU"},
        }
        self.check_error("Duplicate keys detected")

    def test_invalid_mapping_value(self):
        self.config.mappings = {"country": {"EUROVISION": "EU"}}
        self.check_error("for dimension 'country' not found")

    def test_invalid_mapping_value_duplicate(self):
        self.config.mappings = {"country": {"EU27_2020": "EU", "eu27_2020": "EU"}}
        self.check_error("Duplicate values detected")

    def test_duplicate_observations(self):
        self.config.mappings = {"period": {"2013": "2010"}}
        self.check_error("Duplicate key detected in the dataset")

    def test_invalid_period(self):
        self.config.period_start = 2015
        self.config.period_end = 2013
        self.check_error("Start period must be less than or equal to the end period")
