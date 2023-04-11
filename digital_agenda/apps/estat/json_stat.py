"""Simple parser for the JSON-stat format

Full specifications here: https://json-stat.org/format/
"""
import itertools
import functools
import collections
import logging
import math

logger = logging.getLogger(__name__)

Category = collections.namedtuple("Category", ["id", "label"])
Dimension = collections.namedtuple("Dimension", ["id", "label", "categories"])


class JSONStat:
    def __init__(self, dataset):
        self.dataset = dataset
        logger.debug(
            "Parsing JSON-stat: version=%r source=%r label=%r",
            self._version,
            self.source,
            self.label,
        )
        assert self._version >= 2.0, f"Unsupported version: {self._version}"

    @property
    def label(self):
        return self.dataset.get("label", "")

    @property
    def source(self):
        return self.dataset.get("source", "")

    @property
    def _version(self):
        return float(self.dataset.get("version", "nan"))

    @functools.cached_property
    def dimensions(self):
        logger.debug("Parsing dimensions: %s", self.dataset["dimension"])
        result = []
        for dim_id in self.dataset["id"]:
            cat_ids = self.dataset["dimension"][dim_id]["category"]["index"]
            cat_labels = self.dataset["dimension"][dim_id]["category"]["label"]
            if isinstance(cat_ids, dict):
                cat_ids = sorted(cat_ids.keys(), key=lambda i: cat_ids[i])

            result.append(
                Dimension(
                    id=dim_id.lower(),
                    label=self.dataset["dimension"][dim_id].get("label"),
                    categories=[
                        Category(id=cat_id.lower(), label=cat_labels[cat_id])
                        for cat_id in cat_ids
                    ],
                )
            )
        return result

    @functools.cached_property
    def dimension_ids(self):
        return [d.id for d in self.dimensions]

    @functools.cached_property
    def dimension_dict(self):
        return {
            d.id: {cat.id: cat.label for cat in d.categories} for d in self.dimensions
        }

    def _get(self, key, index):
        try:
            if isinstance(self.dataset[key], list):
                return self.dataset[key][index]
            else:
                return self.dataset[key].get(str(index))
        except KeyError:
            return None

    def __iter__(self):
        ranges = [range(id_size) for id_size in self.dataset["size"]]

        for datapoint_index, dim_indexes in enumerate(itertools.product(*ranges)):
            item = {}

            for dim_index, category_index in enumerate(dim_indexes):
                dim = self.dimensions[dim_index]
                item[dim.id] = dim.categories[category_index]

            item["value"] = self._get("value", datapoint_index)
            item["status"] = self._get("status", datapoint_index)

            yield item

    @functools.cached_property
    def length(self):
        return math.prod(self.dataset["size"])

    def __len__(self):
        return self.length
