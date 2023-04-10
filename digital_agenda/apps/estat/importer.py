import datetime
import gzip
import itertools
import shutil
import logging
from functools import cached_property
from collections import defaultdict

import httpx
from django.conf import settings

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import DataSource
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.models import Unit
from digital_agenda.apps.estat.json_stat import JSONStat

logger = logging.getLogger(__name__)

MODELS = {
    "indicator": Indicator,
    "breakdown": Breakdown,
    "country": Country,
    "unit": Unit,
    "period": Period,
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

        if not dataset:
            dataset = self.download()

        self.annotations = {}
        for item in dataset["extension"]["annotation"]:
            self.annotations[item["type"]] = item
        logger.debug("Extracted annotations: %s", self.annotations)

    def download(self):
        logger.info("Getting metadata from: %s", self.download_url)
        with httpx.get(
            self.download_url, timeout=settings.ESTAT_DOWNLOAD_TIMEOUT
        ) as resp:
            resp.raise_for_status()
            return resp.json()

    @cached_property
    def download_url(self):
        # See https://wikis.ec.europa.eu/display/EUROSTATHELP/API+SDMX+2.1+-+metadata+query
        return f"{settings.ESTAT_DOWNLOAD_BASE_URL}/dataflow/{self.code}?format=JSON&lang=en"

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


class EstatDataset(JSONStat):
    def __init__(self, code, force_download=False):
        self.code = code
        self.force_download = force_download
        self.download()

        logger.info("Processing dataset: %s", self.json_path)
        with self.json_path.open() as f:
            super().__init__(f)

    def download(self):
        # XXX This downloads the whole dataset; if this proves to be too large
        # XXX in practice (e.g. because of too much memory used) we can instead:
        # XXX   - split the download per years using the start/endPeriod filter
        # XXX   - filter the download using the provided keys filters
        if not self.force_download and self.json_path.is_file():
            logger.info("File already downloaded: %s", self.json_path)
            return

        logger.info("Downloading from: %s", self.download_url)
        with httpx.stream(
            "GET", self.download_url, timeout=settings.ESTAT_DOWNLOAD_TIMEOUT
        ) as resp:
            with self.download_gz_path.open("wb") as f_out:
                for chunk in resp.iter_raw():
                    f_out.write(chunk)
                resp.raise_for_status()

        logger.info("Decompressing JSON: %s", self.code)
        with gzip.open(self.download_gz_path, "rb") as f_in:
            with self.json_path.open("wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

    @cached_property
    def json_path(self):
        return settings.ESTAT_DOWNLOAD_DIR / f"{self.code}.json"

    @cached_property
    def download_gz_path(self):
        return settings.ESTAT_DOWNLOAD_DIR / f"{self.code}.json.gz"

    @cached_property
    def download_url(self):
        # See https://wikis.ec.europa.eu/display/EUROSTATHELP/API+SDMX+2.1+-+data+query
        return f"{settings.ESTAT_DOWNLOAD_BASE_URL}/data/{self.code}?compressed=true&format=JSON&lang=en"

    @cached_property
    def dataflow(self):
        return EstatDataflow(self.code, dataset=self.dataset)


class EstatImporter:
    def __init__(self, config, force_download=False):
        self.config = config
        self.force_download = force_download
        self.cache = defaultdict(dict)
        self.unique = set()

    @cached_property
    def dataset(self):
        return EstatDataset(self.config.code, force_download=self.force_download)

    @cached_property
    def data_source(self):
        return DataSource.objects.get_or_create(
            code=f"estat_{self.config.code}",
            defaults={
                "label": self.dataset.label,
                "url": f"https://ec.europa.eu/eurostat/web/products-datasets/-/{self.config.code}",
            },
        )[0]

    def should_store_observation(self, obs):
        # Skip empty facts with no flags
        if obs["value"] is None and not obs["status"]:
            return False

        # Apply period filters
        period = int(obs[self.config.period].id)
        if self.config.period_start and self.config.period_start > period:
            return False
        if self.config.period_end and self.config.period_end < period:
            return False

        # Apply all the other filters
        for filter_key, filter_values in self.config.ci_filters.items():
            if obs[filter_key].id.lower() not in filter_values:
                return False

        return True

    def get_dimension_obj(self, dimension, obs):
        config_dim = getattr(self.config, dimension)
        is_surrogate = getattr(self.config, f"{dimension}_is_surrogate")

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

        try:
            return self.cache[dimension][category_id]
        except KeyError:
            obj, created = MODELS[dimension].objects.get_or_create(
                code=category_id, defaults={"label": category_label}
            )
            if created:
                logger.info("Created %r", obj)
            else:
                logger.debug("Using %r", obj)
            self.cache[dimension][category_id] = obj
        return obj

    def get_fact(self, obs):
        fact = Fact(
            value=obs["value"],
            flags=obs["status"] or "",
            import_config_id=self.config.id,
        )
        unique_key = []
        for attr in MODELS:
            obj = self.get_dimension_obj(attr, obs)
            unique_key.append(obj)
            setattr(fact, attr, obj)

        key = tuple(unique_key)
        if key in self.unique:
            raise ImporterError(
                {
                    "Duplicate key detected in the dataset (mapping or filter may not be correct?)": list(
                        map(str, key)
                    )
                }
            )
        self.unique.add(key)

        return fact

    def iter_facts(self):
        for obs in self.dataset:
            if not self.should_store_observation(obs):
                continue

            yield self.get_fact(obs)

    def create_batch(self, facts):
        return Fact.objects.bulk_create(
            facts,
            update_conflicts=True,
            update_fields=("value", "flags", "import_config"),
            unique_fields=("indicator", "breakdown", "unit", "country", "period"),
        )

    def run(self, batch_size=10_000):
        self.config.clean()
        self.config.clean_with_dataset(self.dataset)

        logger.info("Importing with %r", self.config)

        total = 0
        for facts in batched(self.iter_facts(), batch_size):
            total += len(self.create_batch(facts))
            logger.info(
                "Batch processed %r; fact objs created in total %s", self.config, total
            )

        logger.info("Assigning indicator datasource")
        for indicator in self.cache["indicator"].values():
            indicator.data_sources.add(self.data_source)

        logger.info(
            "Import complete %r; processed %s out of %s total in the ESTAT dataset",
            self.config,
            total,
            len(self.dataset),
        )

        self.config.data_last_update = self.dataset.dataflow.update_data
        self.config.datastructure_last_update = self.dataset.dataflow.update_structure
        self.config.datastructure_last_version = self.dataset.dataflow.version
        self.config.save()
