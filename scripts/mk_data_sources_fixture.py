import argparse
import json

import xlrd


def make_fixture(excel_file, output_path):
    cols = (
        "code",
        "label",
        "definition",
        "url",
        "note",
    )

    data = []
    record = {"model": "core.datasource", "fields": None}

    wb = xlrd.open_workbook(excel_file)
    ws = wb.sheet_by_index(0)
    for row_no in range(1, ws.nrows):
        code = ws.cell(row_no, 0).value.strip().lower()
        if not code:
            break

        fields = {"code": code}
        fields.update(
            {
                cols[col_no + 1]: ws.cell(row_no, col_no + 1).value
                for col_no, col in enumerate(cols[1:])
            }
        )
        rec = record.copy()
        rec["fields"] = fields
        data.append(rec)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Make data sources fixture from old site Excel export"
    )
    parser.add_argument("excel_file")
    parser.add_argument("--output", default="datasources.json")
    args = parser.parse_args()
    make_fixture(args.excel_file, args.output)
