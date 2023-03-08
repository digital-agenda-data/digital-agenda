from abc import ABC, abstractmethod
from collections import defaultdict
import logging

from django.db import transaction
import xlrd
import openpyxl

from .models import Period, Country, Indicator, Breakdown, Unit, Fact


logger = logging.getLogger(__name__)


DIMENSION_MODELS = {
    "indicator": Indicator,
    "breakdown": Breakdown,
    "unit": Unit,
    "country": Country,
    "period": Period,
}


class DimensionCache:
    def __init__(self, model):
        self.model = model
        self.cache = {}

    def get(self, code):
        dimension = self.cache.get(code)
        if not dimension:
            try:
                dimension = self.cache[code] = self.model.objects.get(code=code)
            except self.model.DoesNotExist:
                dimension = None

        return dimension


class BaseFileLoader(ABC):
    """Base class for loading file data into database `Fact`s"""

    def __init__(self, path):
        self.path = path
        self.dimensions = {
            name: DimensionCache(model) for name, model in DIMENSION_MODELS.items()
        }

    @abstractmethod
    def load(self, *args, **kwargs):
        ...


DEFAULT_EXCEL_COLS = (
    "period",
    "country",
    "indicator",
    "breakdown",
    "unit",
    "value",
    "flags",
)


class BaseExcelLoader(BaseFileLoader, ABC):
    """
    Loader for Excel file formats.
    """

    def __init__(self, path, cols=DEFAULT_EXCEL_COLS, extra_fields=None):
        super().__init__(path)
        self.extra_fields = extra_fields or {}
        self.cols = cols
        self.sheet = None

    @property
    @abstractmethod
    def rows_iterator(self):
        """Returns an implementation-specific (xls/xlsx) iterator over the active sheet's rows."""
        ...

    @abstractmethod
    def get_row(self, row_ref):
        """Get a row object using a reference produced by `row_iterator`."""
        ...

    def read_row(self, row):
        """
        Read data from the given row.
        Returns: tuple(dict)
            - a field: value dict ready for use in Fact instance creation
            - a dimension: set of codes dict with unknown dimension codes
        """
        fields = {
            **self.extra_fields,
            "value": row[self.cols.index("value")].value,
            "flags": row[self.cols.index("flags")].value or "",
        }
        errors = defaultdict(set)
        for dim_name, dim_model in DIMENSION_MODELS.items():
            dim_code = row[self.cols.index(dim_name)].value
            fields[dim_name] = self.dimensions[dim_name].get(dim_code)
            if fields[dim_name] is None:
                errors[dim_name].add(dim_code)

        return fields, errors

    @staticmethod
    def empty_cell(cell):
        return cell.value is None or cell.value == ""

    def valid_row(self, row):
        """
        Validate a row's data.
        All dimensions and at least one of value/flags must be present.
        """
        return all(
            [not self.empty_cell(cell) for cell in row[: len(self.cols) - 2]]
        ) and any([not self.empty_cell(cell) for cell in row[len(self.cols) - 2 :: 2]])

    def read(self):
        """
        Read the Excel file until the first invalid row.

        Collects Fact instances into the `data` attribute,
        and unknown dimension values into the `errors` attribute.
        """
        data = []
        errors = defaultdict(set)

        for row_ref in self.rows_iterator:
            row = self.get_row(row_ref)

            # Import until first invalid row
            if not self.valid_row(row):
                break

            fields, row_errors = self.read_row(row)

            # Skip the row if any dimension code is unknown or both value and flags are missing
            if row_errors:
                for dim_name, dim_codes in row_errors.items():
                    errors[dim_name].update(dim_codes)
                continue

            data.append(Fact(**fields))

        return data, errors

    def load(self, allow_errors=False):
        """
        Load the Excel data into `Fact` records.
        If errors are encountered, data is written to the database only if `allow_errors` is set.

        Returns: tuple(int, dict)
            - number of records loaded
            - errors
        """
        data, errors = self.read()

        if not data and not errors:
            return 0, {"issue": "No valid row found"}
        elif errors and not allow_errors:
            return 0, {
                "issue": "Missing dimension codes",
                "details": {k: list(v) for k, v in errors.items()},
            }

        with transaction.atomic():
            facts = Fact.objects.bulk_create(
                data,
                update_conflicts=True,
                update_fields=("value", "flags", "import_file"),
                unique_fields=("indicator", "breakdown", "unit", "country", "period"),
            )
            return len(facts), errors


class XLSLoader(BaseExcelLoader):
    def __init__(self, path, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.wb = xlrd.open_workbook(self.path)
        self.ws = self.wb.sheet_by_index(0)

    def get_row(self, row_ref):
        return self.ws.row(row_ref)

    @property
    def rows_iterator(self):
        return range(1, self.ws.nrows)


class XLSXLoader(BaseExcelLoader):
    def __init__(self, path, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.wb = openpyxl.load_workbook(self.path, read_only=True)
        self.ws = self.wb.active

    def get_row(self, row_ref):
        return row_ref  # openpyxl iter_rows returns actual row objects

    @property
    def rows_iterator(self):
        return self.ws.iter_rows(2, self.ws.max_row, 1, len(self.cols))


def get_loader(data_file, extra_fields=None):

    if data_file.mime_type == "application/vnd.ms-excel":
        return XLSLoader(data_file.path, extra_fields=extra_fields)
    elif (
        data_file.mime_type
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        return XLSXLoader(data_file.path, extra_fields=extra_fields)
    else:
        raise TypeError("Unsupported MIME type")
