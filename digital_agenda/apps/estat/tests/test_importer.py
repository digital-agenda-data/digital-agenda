import json
from unittest.mock import patch

from betamax.fixtures.unittest import BetamaxTestCase
from django.conf import settings
from django.test import TestCase
from openpyxl.reader.excel import load_workbook

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


class BetamaxPatchTestCase(BetamaxTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self._mock_session = patch(
            "requests.sessions.Session", return_value=self.session
        ).start()

    def tearDown(self):
        super().tearDown()
        patch.stopall()


class TestImporterSuccess(BetamaxPatchTestCase):
    fixtures = ["test/geogroup", "test/importconfig.json"]

    def setUp(self):
        super().setUp()
        self.config = ImportConfig.objects.first()
        self.config.run_import(delete_existing=True)
        self.config.refresh_from_db()

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
        self.assertEqual(
            data_source.label,
            "Eurostat, table isoc_ci_cm_h: Households - availability of computers",
        )
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
        expected = ["2010", "2011", "2012", "2013"]
        codes = Period.objects.order_by("code").values_list("code", flat=True)
        labels = Period.objects.order_by("label").values_list("label", flat=True)

        self.assertEqual(expected, list(codes))
        self.assertEqual(expected, list(labels))

    def test_country(self):
        codes = Country.objects.order_by("code").values_list("code", flat=True)

        # It's actually 28 because we expect "EU" as well
        self.assertEqual(len(codes), 28)
        self.assertEqual(EU27_2020, list(codes))


class TestImporterDryRun(BetamaxPatchTestCase):
    fixtures = ["test/geogroup", "test/importconfig.json"]

    def setUp(self):
        super().setUp()
        self.config = ImportConfig.objects.first()
        self.key = ("h_comp", "a1_dch", "pc_hh", "nl", "2010")

    def check_dry_run(self):
        self.config.run_import(dry_run=True)
        self.config.refresh_from_db()
        self.assertEqual(self.config.latest_task.status, "SUCCESS")
        self.assertIsNotNone(self.config.latest_task.dry_run_report)

        wb = load_workbook(self.config.latest_task.dry_run_report.file, read_only=True)
        ws = wb.active

        rows = list(ws.rows)
        headers = [i.value for i in rows[0]]
        values = {}
        for row in rows[1:]:
            row = [i.value for i in row]
            key = tuple(row[:5])
            values[key] = dict(zip(headers, row))
        return values

    def create_fact(self, value, flags):
        return Fact.objects.create(
            import_config=self.config,
            indicator=Indicator.objects.get_or_create(code="h_comp")[0],
            breakdown=Breakdown.objects.get_or_create(code="a1_dch")[0],
            unit=Unit.objects.get_or_create(code="pc_hh")[0],
            country=Country.objects.get_or_create(code="nl")[0],
            period=Period.objects.get_or_create(code="2010")[0],
            value=value,
            flags=flags,
        )

    def test_create(self):
        results = self.check_dry_run()
        row = results[self.key]
        self.assertEqual(row["Change Type"], "CREATE")
        self.assertEqual(row["Old Value"], None)
        self.assertEqual(row["Old Flags"], None)
        self.assertEqual(row["New Value"], 100)
        self.assertEqual(row["New Flags"], "u")
        self.assertEqual(row["Diff"], None)

    def test_verify_no_import_config(self):
        fact = self.create_fact(100, "u")
        fact.import_config = None
        fact.save()

        results = self.check_dry_run()
        row = results[self.key]
        self.assertEqual(row["Change Type"], "NO CHANGE")
        self.assertEqual(row["Old Value"], 100)
        self.assertEqual(row["Old Flags"], "u")
        self.assertEqual(row["New Value"], 100)
        self.assertEqual(row["New Flags"], "u")
        self.assertEqual(row["Diff"], 0)

    def test_verify_no_change(self):
        self.create_fact(100, "u")
        results = self.check_dry_run()
        row = results[self.key]
        self.assertEqual(row["Change Type"], "NO CHANGE")
        self.assertEqual(row["Old Value"], 100)
        self.assertEqual(row["Old Flags"], "u")
        self.assertEqual(row["New Value"], 100)
        self.assertEqual(row["New Flags"], "u")
        self.assertEqual(row["Diff"], 0)

    def test_verify_update_value(self):
        self.create_fact(99, "u")
        results = self.check_dry_run()
        row = results[self.key]
        self.assertEqual(row["Change Type"], "UPDATE value")
        self.assertEqual(row["Old Value"], 99)
        self.assertEqual(row["Old Flags"], "u")
        self.assertEqual(row["New Value"], 100)
        self.assertEqual(row["New Flags"], "u")
        self.assertEqual(row["Diff"], 1)

    def test_verify_update_flags(self):
        self.create_fact(100, "r")
        results = self.check_dry_run()
        row = results[self.key]
        self.assertEqual(row["Change Type"], "UPDATE flags")
        self.assertEqual(row["Old Value"], 100)
        self.assertEqual(row["Old Flags"], "r")
        self.assertEqual(row["New Value"], 100)
        self.assertEqual(row["New Flags"], "u")
        self.assertEqual(row["Diff"], 0)

    def test_verify_delete(self):
        fact = self.create_fact(100, "r")
        fact.indicator = Indicator.objects.get_or_create(code="foo_bar")[0]
        fact.save()

        key = ("foo_bar", "a1_dch", "pc_hh", "nl", "2010")

        results = self.check_dry_run()
        row = results[key]
        self.assertEqual(row["Change Type"], "DELETE")
        self.assertEqual(row["Old Value"], 100)
        self.assertEqual(row["Old Flags"], "r")
        self.assertEqual(row["New Value"], None)
        self.assertEqual(row["New Flags"], None)
        self.assertEqual(row["Diff"], None)


class TestImporter(BetamaxPatchTestCase):
    fixtures = ["test/geogroup", "test/importconfig.json"]

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


class TestImporterDataMerge(BetamaxPatchTestCase):
    fixtures = ["test/geogroup", "test/data_merge_importconfig.json"]

    def setUp(self):
        super().setUp()
        # See https://ec.europa.eu/eurostat/databrowser/view/isoc_e_dii/default/table
        # for values
        self.config = ImportConfig.objects.first()

    def test_raise_error(self):
        self.config.run_import(delete_existing=True)
        self.config.refresh_from_db()
        self.assertIn(
            "Duplicate key detected in the dataset",
            self.config.latest_task.failure_reason,
        )

    def test_sum_values(self):
        self.config.conflict_resolution = ImportConfig.ConflictResolution.SUM_VALUES
        self.config.save()
        self.config.run_import(delete_existing=True)

        fact = Fact.objects.get(
            indicator__code="e_di4_vhi_and_hi",
            breakdown__code="total",
            unit__code="pc_ent",
            period__code="2022",
            country__code="EU",
        )
        # EU should have:
        #   - 4.3 for e_di_vhi
        #   - 28.1 for e_di_hi
        self.assertEqual(fact.value, 32.4)
        self.assertEqual(fact.flags, "")

    def test_avg_values(self):
        self.config.conflict_resolution = ImportConfig.ConflictResolution.AVERAGE_VALUES
        self.config.save()
        self.config.run_import(delete_existing=True)

        fact = Fact.objects.get(
            indicator__code="e_di4_vhi_and_hi",
            breakdown__code="total",
            unit__code="pc_ent",
            period__code="2022",
            country__code="EU",
        )
        # EU should have:
        #   - 4.3 for e_di_vhi
        #   - 28.1 for e_di_hi
        self.assertEqual(fact.value, 16.2)
        self.assertEqual(fact.flags, "")

    def test_missing_value_sum(self):
        self.config.conflict_resolution = ImportConfig.ConflictResolution.SUM_VALUES
        self.config.save()
        self.config.run_import(delete_existing=True)

        fact = Fact.objects.get(
            indicator__code="e_di4_vhi_and_hi",
            breakdown__code="total",
            unit__code="pc_ent",
            period__code="2022",
            country__code="MK",
        )
        # Nort Macedonia (MK) has no value for e_di_vhi
        self.assertEqual(fact.value, None)
        self.assertEqual(fact.flags, "~")

    def test_missing_value_avg(self):
        self.config.conflict_resolution = ImportConfig.ConflictResolution.AVERAGE_VALUES
        self.config.save()
        self.config.run_import(delete_existing=True)

        fact = Fact.objects.get(
            indicator__code="e_di4_vhi_and_hi",
            breakdown__code="total",
            unit__code="pc_ent",
            period__code="2022",
            country__code="MK",
        )
        # Nort Macedonia (MK) has no value for e_di_vhi
        self.assertEqual(fact.value, None)
        self.assertEqual(fact.flags, "~")

    def test_merge_flags(self):
        self.config.conflict_resolution = ImportConfig.ConflictResolution.SUM_VALUES
        self.config.save()
        self.config.run_import(delete_existing=True)

        fact = Fact.objects.get(
            indicator__code="e_di4_vhi_and_hi",
            breakdown__code="total",
            unit__code="pc_ent",
            period__code="2022",
            country__code="FR",
        )
        # France (FR) has the (b) flag for both values
        self.assertEqual(fact.flags, "b")


class TestImporterErrors(BetamaxPatchTestCase):
    fixtures = ["test/geogroup", "test/importconfig.json"]

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
