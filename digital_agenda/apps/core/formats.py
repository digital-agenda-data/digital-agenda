import decimal
from abc import ABC, abstractmethod
from collections import defaultdict
import logging

from django.db import transaction
import xlrd
import openpyxl
from openpyxl.utils import get_column_letter

from .models import Period, Country, Indicator, Breakdown, Unit, Fact
from .views.facts import EUROSTAT_FLAGS

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
        # Period obj can be auto-created
        self._auto_create = model == Period

    def get(self, code):
        try:
            return self.cache[code]
        except KeyError:
            pass

        if self._auto_create:
            obj = self.cache[code] = self.model.objects.get_or_create(code=code)[0]
        else:
            try:
                obj = self.cache[code] = self.model.objects.get(code=code)
            except (self.model.DoesNotExist, ValueError):
                obj = None

        return obj


class BaseFileLoader(ABC):
    """Base class for loading file data into database `Fact`s"""

    def __init__(self, path):
        self.path = path
        self.dimensions = {
            name: DimensionCache(model) for name, model in DIMENSION_MODELS.items()
        }

    @abstractmethod
    def load(self, *args, **kwargs): ...


DEFAULT_EXCEL_COLS = (
    "period",
    "country",
    "indicator",
    "breakdown",
    "unit",
    "value",
    "flags",
)


class RowReader:
    def __init__(
        self,
        row,
        dimensions,
        cols=DEFAULT_EXCEL_COLS,
        extra_fields=None,
        required_cols=None,
    ):
        self.dimensions = dimensions
        self.row = row
        self.cols = cols
        # By default, all columns are required except for value and flags
        self.required_cols = required_cols or self.cols[:-2]
        self.errors = defaultdict(list)
        self.fields = {**extra_fields}
        self.read_row()

    def add_error(self, col_index, error):
        col_letter = get_column_letter(col_index + 1)
        self.errors[f"Column {col_letter}"].append(error)

    def get_value(self):
        col_index = self.cols.index("value")
        value_cell = self.row[col_index]

        value = value_cell.value
        if self.empty_cell(value_cell):
            value = None

        if value is not None:
            try:
                # Excel can sometimes store values like 5.6621000000000006 while only
                # displaying 5.6621.
                # Round to a sensible precision to (hopefully) get rid of the issue.
                value = float(round(decimal.Decimal(value), 6))
            except (TypeError, ValueError, ArithmeticError):
                self.add_error(
                    col_index,
                    f"Invalid 'value', expected number but got {value!r} instead",
                )

        return value

    def get_flags(self):
        col_index = self.cols.index("flags")
        flags_cell = self.row[col_index]

        flags = flags_cell.value or ""
        for flag in flags:
            if flag not in EUROSTAT_FLAGS:
                self.add_error(col_index, f"Unknown flag {flag!r}")

        return flags

    def read_row(self):
        """
        Read data from the given row.
        """
        self.fields["value"] = self.get_value()
        self.fields["flags"] = self.get_flags()

        if self.fields["value"] is None and not self.fields["flags"]:
            # Set the custom flag "unavailable" for this case
            self.fields["flags"] = "x"

        for col in self.required_cols:
            col_index = self.cols.index(col)
            cell = self.row[col_index]

            if self.empty_cell(cell):
                self.add_error(col_index, f"Column {col!r} must not be empty")

        for dim_name, dim_model in DIMENSION_MODELS.items():
            col_index = self.cols.index(dim_name)
            dim_code = self.row[col_index].value

            self.fields[dim_name] = self.dimensions[dim_name].get(dim_code)
            if self.fields[dim_name] is None:
                self.add_error(
                    col_index, f"Missing dimension code for {dim_name!r}: {dim_code!r}"
                )

    @staticmethod
    def empty_cell(cell):
        return cell.value is None or cell.value == ""


class BaseExcelLoader(BaseFileLoader, ABC):
    """
    Loader for Excel file formats.
    """

    def __init__(
        self, path, cols=DEFAULT_EXCEL_COLS, extra_fields=None, required_cols=None
    ):
        super().__init__(path)
        self.extra_fields = extra_fields or {}
        self.cols = cols
        # By default, all columns are required except for value and flags
        self.required_cols = required_cols or self.cols[:-2]
        self.sheet = None
        self.errors = {}

    @property
    @abstractmethod
    def rows_iterator(self):
        """Returns an implementation-specific (xls/xlsx) iterator over the active sheet's rows."""
        ...

    @abstractmethod
    def get_row(self, row_ref):
        """Get a row object using a reference produced by `row_iterator`."""
        ...

    def read(self):
        """
        Read the all rows from Excel file.

        Collects Fact instances into the `data` attribute,
        and unknown dimension values into the `errors` attribute.
        """
        data = []
        errors = {}
        all_unique_keys = {}

        for row_index, row_ref in enumerate(self.rows_iterator, start=1):
            row_reader = RowReader(
                self.get_row(row_ref),
                self.dimensions,
                cols=self.cols,
                extra_fields=self.extra_fields,
                required_cols=self.required_cols,
            )

            unique_key = tuple(row_reader.fields[field] for field in self.required_cols)
            if duplicate_row := all_unique_keys.get(unique_key):
                row_reader.errors["ALL"].append(
                    f"Duplicate entry found at Row {duplicate_row}"
                )
            all_unique_keys[unique_key] = row_index

            # Skip the row if any dimension code is unknown or both value and flags are missing
            if row_reader.errors:
                errors[f"Row {row_index}"] = dict(row_reader.errors)
                continue

            data.append(Fact(**row_reader.fields))

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
            return 0, errors

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
