"""
Helpers for using the Eurostat bulk download facilities
"""
from functools import cached_property
from collections import defaultdict
import csv
import io
import gzip
import logging
import shutil
from typing import Dict, List, Optional, Tuple, Union, Any

from attrs import define
from django.conf import settings
import httpx
import pandas as pd

logger = logging.getLogger(__name__)


@define(slots=False, kw_only=True)
class BulkFile:
    url: str
    filename: str

    @property
    def path(self):
        return settings.BULK_DOWNLOAD_DIR / self.filename

    def download(self):
        with io.BytesIO() as download_stream:
            try:
                with httpx.stream("GET", self.url) as response:
                    for chunk in response.iter_raw():
                        download_stream.write(chunk)
                    response.raise_for_status()
            except httpx.RequestError as exc:
                logger.error(
                    "An error occurred while requesting %s - %s",
                    exc.request.url,
                    str(exc),
                )
                return None
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "Error response %s while requesting %s",
                    exc.response.status_code,
                    exc.request.url,
                )
                return None

            # Bulk download responses are gzipped.
            # Additionally, some files are gzip archives,
            # thus we need recursive decompression:

            def decompress_to_disk(fileobj):
                fileobj.seek(0)
                with gzip.open(fileobj, "rb") as gz:
                    try:
                        if gz.read(2) != b"\x1f\x8b":  # gzip magic number
                            raise gzip.BadGzipFile()
                        # Make another attempt, in case the data is compressed multiple times
                        decompress_to_disk(gz)
                    except gzip.BadGzipFile:
                        logger.debug(
                            "Bulk file %s downloaded to %s", self.url, self.path
                        )
                        gz.seek(0)
                        with open(self.path, "wb") as out:
                            shutil.copyfileobj(gz, out)

            decompress_to_disk(download_stream)

        return self.path


def bulk_dict_url(dic, lang="en"):
    return f"{settings.BULK_DOWNLOAD_ROOT_URL}?sort=1&downfile=dic/{lang}/{dic}.dic"


DATASETS_FILE = BulkFile(
    url=bulk_dict_url("table_dic"),
    filename="table_dic.dic",
)

DIMENSIONS_FILE = BulkFile(
    url=bulk_dict_url("dimlst"),
    filename="dimlst.dic",
)

METABASE_FILE = BulkFile(
    url=f"{settings.BULK_DOWNLOAD_ROOT_URL}?sort=1&downfile=metabase.txt.gz",
    filename="metabase.txt",
)


# Dimensions and their values allow gradual definition, outside the mandatory code.


@define
class DimensionValue:
    code: str
    label: Optional[str] = None


@define
class Dimension:
    code: str
    label: Optional[str] = None
    lowest: Optional[bool] = False
    values: Optional[Dict[str, DimensionValue]] = None


@define(slots=False, kw_only=True)
class BulkTSVDataset(BulkFile):
    name: str
    url: Optional[str] = None
    filename: Optional[str] = None

    SPECIAL_VALUE = ":"

    def __attrs_post_init__(self):
        self.filename = self.filename or f"{self.name.lower()}.tsv"
        self.url = (
            self.url
            or f"{settings.BULK_DOWNLOAD_ROOT_URL}?sort=1&downfile=data/{self.name.lower()}.tsv.gz"
        )

    @cached_property
    def label(self):
        """
        Obtain the dataset label from the datasets/tables bulk file.
        If not present locally, the file is downloaded first.
        """
        if not DATASETS_FILE.path.exists():
            datasets_file = DATASETS_FILE.download()
            if datasets_file is None:
                raise RuntimeError("Could not download datasets (tables) bulk file")

        label = None
        with open(DATASETS_FILE.path, newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if row[0].lower() == self.name.lower():
                    return row[1]

        return label

    @cached_property
    def dimensions(self):
        """
        Read the dimensions from the dataset's header.
        """
        if not self.path.exists():
            self.download()

        with open(self.path, newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            header = next(reader)
            # Dimensions names are in the first row+col, comma-separated, except
            # for the series (lowest) dimension, which is slash-separated from the rest,
            # e.g.: 'unit,isced11,sex,geo\time'.
            dimensions = header[0].split(",")
            dimensions[-1], series_dim = dimensions[-1].split("\\")
            dimensions.append(series_dim)
            return {
                d: Dimension(code=d, lowest=not (di + 1 < len(dimensions)))
                for di, d in enumerate(dimensions)
            }

    @cached_property
    def dimension_codes(self):
        return list(self.dimensions.keys())

    @cached_property
    def series_dimension(self):
        for dk, d in self.dimensions.items():
            if d.lowest:
                return d

        return None

    @cached_property
    def metadata(self):
        """
        Read the dimension codes used in the dataset, from the metabase bulk file.
        If not present locally, the file is downloaded first.
        """
        if not METABASE_FILE.path.exists():
            metabase_path = METABASE_FILE.download()
            if metabase_path is None:
                raise RuntimeError(
                    "Could not download metabase bulk file %s", METABASE_FILE.filename
                )

        meta = defaultdict(set)
        with open(METABASE_FILE.path, newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if row[0].lower() == self.name.lower():
                    meta[row[1]].add(row[2])

        return meta

    def populate_dimension_labels(self):
        if not DIMENSIONS_FILE.path.exists():
            dims_file = DIMENSIONS_FILE.download()
            if dims_file is None:
                raise RuntimeError("Could not download dimensions bulk file")

        with open(DIMENSIONS_FILE.path, newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                dim, label = row[0].lower(), row[1]
                if dim in self.dimension_codes:
                    self.dimensions[dim].label = label

    def populate_dimension_values(self):
        for dim_code in self.dimensions:
            dim_file = BulkFile(
                url=bulk_dict_url(dim_code),
                filename=f"{dim_code}.dic",
            )
            if not dim_file.path.exists():
                dim_file_path = dim_file.download()
                if dim_file_path is None:
                    raise RuntimeError(
                        "Could not download dimension %s bulk codes file", dim_code
                    )

            dim_values = self.metadata[dim_code]

            self.dimensions[dim_code].values = {}

            with open(dim_file.path, newline="") as f:
                reader = csv.reader(f, delimiter="\t")
                for row in reader:
                    code, label = row
                    if code in dim_values:
                        self.dimensions[dim_code].values[code] = DimensionValue(
                            code=code, label=label
                        )

            # In case dimension values are NOT present in the dimension table,
            # add them without a label (e.g. year values).
            missing_dim_vals = [
                dim_v
                for dim_v in dim_values
                if dim_v not in self.dimensions[dim_code].values
            ]
            for missing_val in missing_dim_vals:
                self.dimensions[dim_code].values[missing_val] = DimensionValue(
                    code=missing_val, label=""
                )

    def get_data(self):
        data = []

        with open(self.path, newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            header = next(reader)
            # First row had values for the series/lower dimension from the second column forward.
            series_dim_data = [v.strip() for v in header[1:]]

            for row in reader:
                row_dims = row[0].split(",")
                for col, fact in enumerate(row[1:]):
                    # Fact "cells" are space-separated pairs of a value and a set of flags.
                    # Flags are represented as single characters, and when more are present
                    # they form a string, e.g.: "bu".
                    val, flags = fact.split(" ")
                    val = float(val) if val != BulkTSVDataset.SPECIAL_VALUE else None
                    # Skip empty facts (no value or flag(s))
                    if val is not None or flags:
                        data.append((*row_dims, series_dim_data[col], val, flags))

        return data

    data = cached_property(get_data)

    def to_df(self, sparse: bool = False) -> pd.DataFrame:
        """
        Reads a TSV bulk Eurostat dataset and returns a DataFrame.

        Args:
            sparse (bool): Toggle for including measurements where both value and flags are missing.

        Returns:
            pandas.DataFrame:
        """

        df = pd.DataFrame(
            self.data,
            columns=self.dimension_codes
            + ["val", "flag"],  # NOT 'flags', to avoid collision with DataFrame.flags
        )
        df.set_index(self.dimension_codes, inplace=True)

        return df


@define
class BulkSDMXDataset(BulkFile):
    name: str
    url: Optional[str] = None
    dirname: Optional[str] = None
    filename: Optional[str] = None
    schema_filename: Optional[str] = None

    def __attrs_post_init__(self):
        self.dirname = self.dirname or f"{self.name.lower()}.sdmx"
        self.filename = self.filename or f"{self.name.lower()}.sdmx.xml"
        self.schema_filename = self.schema_filename or f"{self.name.lower()}.dsd.xml"
        self.url = (
            self.url
            or f"{settings.BULK_DOWNLOAD_ROOT_URL}?sort=1&downfile=data/{self.name.lower()}.sdmx.zip"
        )

    @property
    def schema_path(self):
        return settings.BULK_DOWNLOAD_DIR / self.schema_filename
