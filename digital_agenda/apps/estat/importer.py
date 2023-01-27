import gzip
import itertools
import shutil
import logging
from functools import cached_property
from collections import defaultdict

import httpx
from django.conf import settings
from django.core.exceptions import ValidationError

from digital_agenda.apps.core.models import Breakdown
from digital_agenda.apps.core.models import Country
from digital_agenda.apps.core.models import DataSource
from digital_agenda.apps.core.models import Fact
from digital_agenda.apps.core.models import Indicator
from digital_agenda.apps.core.models import Period
from digital_agenda.apps.core.models import Unit
from digital_agenda.apps.estat.json_stat import JSONStat
from digital_agenda.apps.estat.models import ImportConfig

logger = logging.getLogger(__name__)

MODELS = {
    "indicator": Indicator,
    "breakdown": Breakdown,
    "country": Country,
    "unit": Unit,
    "period": Period,
}


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


class EstatImporter:
    def __init__(self, config_id, force_download=False):
        self.config = ImportConfig.objects.get(pk=config_id)
        self.force_download = force_download
        self.cache = defaultdict(dict)
        self.unique = set()

    @cached_property
    def dataset(self):
        self.download()

        logger.info("Processing dataset: %s", self.json_path)
        with self.json_path.open() as f:
            return JSONStat(f)

    def download(self):
        # XXX This downloads the whole dataset; if this proves to be too large
        # XXX in practice (e.g. because of too much memory used) we can instead:
        # XXX   - split the download per years using the start/endPeriod filter
        # XXX   - filter the download using the provided keys filters
        if not self.force_download and self.json_path.is_file():
            logger.info("File already downloaded: %s", self.json_path)
            return

        logger.info("Downloading from: %s", self.download_url)
        with httpx.stream("GET", self.download_url) as resp:
            with self.download_gz_path.open("wb") as f_out:
                for chunk in resp.iter_raw():
                    f_out.write(chunk)
                resp.raise_for_status()

        logger.info("Decompressing JSON: %s", self.config.code)
        with gzip.open(self.download_gz_path, "rb") as f_in:
            with self.json_path.open("wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

    @cached_property
    def json_path(self):
        return settings.ESTAT_DOWNLOAD_DIR / f"{self.config.code}.json"

    @cached_property
    def download_gz_path(self):
        return settings.ESTAT_DOWNLOAD_DIR / f"{self.config.code}.json.gz"

    @cached_property
    def download_url(self):
        # See https://wikis.ec.europa.eu/display/EUROSTATHELP/API+SDMX+2.1+-+data+query
        return f"{settings.ESTAT_DOWNLOAD_BASE_URL}/{self.config.code}?compressed=true&format=JSON&lang=en"

    @cached_property
    def data_source(self):
        return DataSource.objects.get_or_create(
            code=f"estat_{self.config.code}",
            defaults={
                "label": self.dataset.label,
                "url": f"https://ec.europa.eu/eurostat/web/products-datasets/-/{self.config.code}",
            },
        )[0]

    @cached_property
    def ci_filters(self):
        """Convert the filters specified in the import config into lower-cased
        sets, to be used for case insensitive checks.
        """
        result = {}

        for key, values in self.config.filters.items():
            result[key] = set([val.lower() for val in values])

        # Update the "country" dimension filter (usually geo) with
        # the configured country group filter if available.
        if self.config.country_group:
            if self.config.country not in result:
                result[self.config.country] = set()

            result[self.config.country].update(
                set(
                    [val.lower() for val in self.config.country_group.geo_codes]
                    + [self.config.country_group.code.lower()]
                )
            )

        return result

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
        for filter_key, filter_values in self.ci_filters.items():
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
                category_id = self.config.mappings[dimension][category_id]
            except KeyError:
                pass

        try:
            return self.cache[dimension][category_id]
        except KeyError:
            obj, _created = MODELS[dimension].objects.get_or_create(
                code=category_id,
                defaults={
                    "label": category_label,
                },
            )
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
            raise ValidationError(
                f"Duplicate key detected in the dataset "
                f"(mapping or filter may not be correct?): {key}"
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
                "Batch processed %r; fact objs created %s / %s",
                self.config,
                total,
                len(self.dataset),
            )

        logger.info("Assigning indicator datasource")
        for indicator in self.cache["indicator"].values():
            indicator.data_source = self.data_source
            indicator.save()
