import collections
import datetime
import gzip
import hashlib
import itertools
import json
import shutil
import logging
import decimal
from functools import cached_property
from collections import defaultdict
from io import BytesIO
from typing import TYPE_CHECKING
from urllib.parse import urlencode

import openpyxl
import requests
from django.conf import settings
from django.utils.text import get_valid_filename

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import DataSource
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.models import Unit
from digital_agenda.apps.estat.json_stat import JSONStat


if TYPE_CHECKING:
    from digital_agenda.apps.estat.models import ImportConfig

logger = logging.getLogger(__name__)

MODEL_DIMENSIONS = {
    "indicator": Indicator,
    "breakdown": Breakdown,
    "country": Country,
    "unit": Unit,
    "period": Period,
}
TEXT_DIMENSION = (
    "reference_period",
    "remarks",
)

ESTAT_HEADERS = {
    # XXX Normally requests put "gzip, deflate" here and handles
    # XXX decompressing stuff transparently. HOWEVER!! While EUROSTAT
    # XXX checks the Accept-Encoding header, it DOES NOT put the
    # XXX "Content-Encoding" in the response. So request assumes the server
    # XXX doesn't have compression capabilities and assumes it's plaintext.
    "Accept-Encoding": "identity",
    "Accept": "application/json",
}


class ImporterError(ValueError):
    pass


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter.

    batched('ABCDEFG', 3) --> ABC DEF G
    """
    # Based on https://docs.python.org/3/library/itertools.html#itertools-recipes
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


class EstatDataflow:
    def __init__(self, code, dataset=None):
        self.code = code
        self.dataset = dataset
        if not self.dataset:
            self.download()

        self.annotations = {}
        for item in self.dataset["extension"]["annotation"]:
            self.annotations[item["type"]] = item
        logger.debug("Extracted annotations: %s", self.annotations)

    def download(self):
        logger.info("Getting metadata from: %s", self.download_url)
        session = requests.Session()
        resp = session.get(
            self.download_url,
            timeout=settings.ESTAT_DOWNLOAD_TIMEOUT,
            headers=ESTAT_HEADERS,
        )
        resp.raise_for_status()
        self.dataset = resp.json()

    @cached_property
    def download_url(self):
        # See https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/sdmx3-0/structure-queries
        return f"{settings.ESTAT_DOWNLOAD_BASE_URL}/structure/dataflow/ESTAT/{self.code}/1.0/?lang=EN&format=JSON"

    @cached_property
    def version(self):
        return self.dataset["extension"]["datastructure"]["version"]

    @cached_property
    def update_data(self):
        return datetime.datetime.fromisoformat(self.annotations["UPDATE_DATA"]["date"])

    @cached_property
    def update_structure(self):
        return datetime.datetime.fromisoformat(
            self.annotations["UPDATE_STRUCTURE"]["date"]
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.version == other.version
            and self.update_data == other.update_data
            and self.update_structure == other.update_structure
        )

    def __str__(self):
        return f"<ESTAT Dataflow(code={self.code}, version={self.version})>"


class EstatDataset(JSONStat):
    def __init__(self, config: "ImportConfig", force_download=False):
        self.config = config
        self.code = self.config.code
        self.force_download = force_download
        self._cached_dataset = None

        self._load_cached()
        if self._cache_is_stale:
            self._download()
            self._load_cached()

        logger.info("Processing dataset: %s", self.json_path)
        super().__init__(self._cached_dataset)

    def _download(self):
        logger.info("Downloading from: %s", self.download_url)
        session = requests.Session()
        with session.get(
            self.download_url,
            timeout=settings.ESTAT_DOWNLOAD_TIMEOUT,
            stream=True,
            headers=ESTAT_HEADERS,
        ) as resp:
            if resp.status_code == 400:
                # An HTTP 400 usually has additional information on what was wrong.
                # For example, a bad value for a filter, so extract it and add it here.
                # Instead of just logging the generic error requests gives.
                raise ImporterError(resp.json())
            with self.json_path.open("wb") as f_out:
                for chunk in resp.iter_content(chunk_size=512):
                    f_out.write(chunk)
                resp.raise_for_status()

    def _load_cached(self):
        if self.json_path.is_file():
            with self.json_path.open() as f:
                try:
                    self._cached_dataset = json.load(f)
                except json.JSONDecodeError as e:
                    logger.warning("Cache dataset is corrupted: %s", e)

    @property
    def _cache_is_stale(self):
        if self.force_download:
            logger.info(
                "Cached dataset forced stale: force_download=%s", self.force_download
            )
            return True

        if not self._cached_dataset:
            logger.info("No cached dataset available")
            return True

        old_dataflow = EstatDataflow(self.code, dataset=self._cached_dataset)
        logger.info("Cached dataset %s available, checking if stale", old_dataflow)

        new_dataflow = EstatDataflow(self.code)
        if old_dataflow != new_dataflow:
            logger.info("Cached dataset IS stale, new dataset found: %s", new_dataflow)
            return True

        logger.info("Cached dataset %s is NOT stale", new_dataflow)
        return False

    @cached_property
    def json_path(self):
        filter_hash = hashlib.md5(self.download_url.encode()).hexdigest()
        filename = get_valid_filename(self.code + "-" + filter_hash) + ".json"
        return settings.ESTAT_DOWNLOAD_DIR / filename

    @cached_property
    def download_url(self):
        # See https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/sdmx3-0/data-query
        endpoint = f"/data/dataflow/ESTAT/{self.code}/1.0/"
        args = {"lang": "EN", "format": "JSON"}
        for key_name, values in self.config.filters.items():
            key_name = f"c[{key_name}]"
            args[key_name] = ",".join(values)
        return settings.ESTAT_DOWNLOAD_BASE_URL + endpoint + "?" + urlencode(args)

    @cached_property
    def dataflow(self):
        return EstatDataflow(self.code, dataset=self.dataset)


class EstatImporter:
    def __init__(self, config, force_download=False):
        self.config = config
        self.force_download = force_download
        self.cache = defaultdict(dict)

    @cached_property
    def dataset(self):
        return EstatDataset(self.config, force_download=self.force_download)

    @cached_property
    def data_source(self):
        return DataSource.objects.get_or_create(
            code=f"estat_{self.config.code}",
            defaults={
                "label": f"Eurostat, table {self.config.code}: {self.dataset.label}",
                "url": f"https://ec.europa.eu/eurostat/web/products-datasets/-/{self.config.code}",
            },
        )[0]

    def should_store_observation(self, obs):
        # Skip empty facts with no flags
        if obs["value"] is None and not obs["status"]:
            return False

        # Apply period filters
        year = int(Period.split_code(obs[self.config.period].id)[0])
        if self.config.period_start and self.config.period_start > year:
            return False
        if self.config.period_end and self.config.period_end < year:
            return False

        # Apply all the other filters
        for filter_key, filter_values in self.config.ci_filters.items():
            if obs[filter_key].id.lower() not in filter_values:
                return False

        return True

    def get_dimension(self, dimension, obs):
        config_dim = getattr(self.config, dimension)
        is_surrogate = getattr(self.config, f"{dimension}_is_surrogate")

        if not config_dim:
            return None, None

        if is_surrogate:
            # Hardcoded value, no label available
            category_id, category_label = config_dim, ""
        else:
            category_id = obs[config_dim].id
            category_label = obs[config_dim].label

            # Apply mapping if available, otherwise keep the original
            try:
                category_id = self.config.ci_mappings[dimension][category_id]
            except KeyError:
                pass

        return category_id, category_label

    def get_dimension_obj(self, dimension, obs):
        category_id, category_label = self.get_dimension(dimension, obs)

        try:
            return self.cache[dimension][category_id]
        except KeyError:
            obj, created = MODEL_DIMENSIONS[dimension].objects.get_or_create(
                code=category_id, defaults={"label": category_label}
            )
            if created:
                logger.info("Created %r", obj)
            else:
                logger.debug("Using %r", obj)
            self.cache[dimension][category_id] = obj
        return obj

    def iter_facts(self):
        fact_collection = collections.defaultdict(list)
        for obs in self.dataset:
            if not self.should_store_observation(obs):
                continue

            fact = Fact(
                value=obs["value"],
                flags=obs["status"] or "",
                import_config_id=self.config.id,
            )

            # Set dimensions with related models
            unique_key = []
            for attr in MODEL_DIMENSIONS:
                obj = self.get_dimension_obj(attr, obs)
                unique_key.append(obj)
                setattr(fact, attr, obj)
            fact_collection[tuple(unique_key)].append(fact)

            # Set text "dimensions"
            for attr in TEXT_DIMENSION:
                dim_id, dim_label = self.get_dimension(attr, obs)
                setattr(fact, attr, dim_id or dim_label)

        for key, fact_group in fact_collection.items():
            yield self._handle_conflict(fact_group, key)

    def _handle_conflict(self, fact_group, key):
        if len(fact_group) == 1:
            return fact_group[0]

        # Chose one fact to work on
        fact = fact_group[0]
        try:
            # Convert to decimal (from string) to avoid janky float arithmetics
            total = sum(decimal.Decimal(str(fact.value)) for fact in fact_group)
        except (TypeError, decimal.InvalidOperation):
            # At least one value is missing, set the merged result to None as well
            # and set custom flags to indicate the missing part
            fact.value = None
            fact.flags = "~"
            return fact

        match self.config.conflict_resolution:
            case self.config.ConflictResolution.SUM_VALUES:
                new_value = total
            case self.config.ConflictResolution.AVERAGE_VALUES:
                new_value = total / len(fact_group)
            case _:
                raise ImporterError(
                    {
                        "Duplicate key detected in the dataset (mapping or filter may not be correct?)": list(
                            map(str, key)
                        )
                    }
                )

        all_flags = [set(fact.flags) for fact in fact_group]

        fact.value = float(new_value)
        fact.flags = "".join(set.union(*all_flags))

        return fact

    def create_batch(self, facts):
        return len(
            Fact.objects.bulk_create(
                facts,
                update_conflicts=True,
                update_fields=(
                    "value",
                    "flags",
                    "import_config",
                    "reference_period",
                    "remarks",
                ),
                unique_fields=(
                    "indicator",
                    "breakdown",
                    "unit",
                    "country",
                    "period",
                ),
            )
        )

    def run(self, batch_size=10_000):
        self.config.clean()
        self.config.clean_with_dataset(self.dataset)

        logger.info("Importing with %r", self.config)

        total = self.create_facts(batch_size=batch_size)
        self.update_config()
        logger.info(
            "Import complete %r; processed %s out of %s total in the ESTAT dataset",
            self.config,
            total,
            len(self.dataset),
        )

    def create_facts(self, batch_size=10_000):
        total = 0
        for facts in batched(self.iter_facts(), batch_size):
            total += self.create_batch(facts)
            logger.info(
                "Batch processed %r; fact objs created in total %s", self.config, total
            )
        return total

    def update_config(self):
        logger.info("Assigning indicator datasource")
        for indicator in self.cache["indicator"].values():
            indicator.data_sources.add(self.data_source)
        self.config.data_last_update = self.dataset.dataflow.update_data
        self.config.datastructure_last_update = self.dataset.dataflow.update_structure
        self.config.datastructure_last_version = self.dataset.dataflow.version
        self.config.new_version_available = False
        self.config.save()


class DryRunEstatImporter(EstatImporter):
    def __init__(self, config, force_download=False):
        super().__init__(config, force_download=force_download)
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.set_headers()
        self.current_facts = self.get_current_facts()

    def get_current_facts(self):
        qs = Fact.objects.filter(import_config=self.config).select_related(
            "indicator", "breakdown", "unit", "country", "period"
        )
        return {fact.unique_key: fact for fact in qs}

    def set_headers(self):
        self.ws.append(
            [
                "Indicator",
                "Breakdown",
                "Unit",
                "Country",
                "Period",
                "Old Flags",
                "New Flags",
                "Old Value",
                "New Value",
                "Diff",
                "Change Type",
            ]
        )
        self.ws.freeze_panes = "A2"

    def create_batch(self, facts):
        count = 0
        for new_fact in facts:
            count += 1
            old_fact = self.current_facts.pop(new_fact.unique_key, None)
            if not old_fact:
                # There might be a fact that has the same unique key, but was not
                # included because it's missing the import_config fk.
                old_fact = Fact.objects.filter(
                    indicator=new_fact.indicator,
                    breakdown=new_fact.breakdown,
                    unit=new_fact.unit,
                    country=new_fact.country,
                    period=new_fact.period,
                ).first()

            if not old_fact:
                change_type = "CREATE"
            elif old_fact.value != new_fact.value:
                change_type = "UPDATE value"
            elif old_fact.flags != new_fact.flags:
                change_type = "UPDATE flags"
            else:
                change_type = "NO CHANGE"

            diff = None
            if old_fact and old_fact.value is not None and new_fact.value is not None:
                diff = new_fact.value - old_fact.value

            self.ws.append(
                [
                    new_fact.indicator.code,
                    new_fact.breakdown.code,
                    new_fact.unit.code,
                    new_fact.country.code,
                    new_fact.period.code,
                    old_fact.flags if old_fact else None,
                    new_fact.flags,
                    old_fact.value if old_fact else None,
                    new_fact.value,
                    diff,
                    change_type,
                ]
            )
        return count

    def create_facts(self, batch_size=10_000):
        total = super().create_facts(batch_size=batch_size)
        for fact in self.current_facts.values():
            self.ws.append(
                [
                    fact.indicator.code,
                    fact.breakdown.code,
                    fact.unit.code,
                    fact.country.code,
                    fact.period.code,
                    fact.flags,
                    None,
                    fact.value,
                    None,
                    None,
                    "DELETE",
                ]
            )
        self.ws.auto_filter.ref = self.ws.dimensions
        return total

    def update_config(self):
        logger.info("Configuration not update when importing to XLSX")

    def get_xlsx(self):
        buffer = BytesIO()
        buffer.name = f"{self.config.code}.xlsx"
        self.wb.save(buffer)
        buffer.seek(0)
        return buffer
