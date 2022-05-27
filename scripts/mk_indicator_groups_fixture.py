import argparse
import datetime
import json

import xlrd


def make_fixture(excel_file, output_path, order_coefficient):
    cols = (
        "code",
        "label",
        "display_order",
    )

    data = []
    record = {"model": "core.indicatorgroup", "fields": None}

    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    wb = xlrd.open_workbook(excel_file)
    ws = wb.sheet_by_index(0)
    for row_no in range(1, ws.nrows):
        code = ws.cell(row_no, 0).value.strip().lower()
        if not code:
            break

        fields = {
            "code": code,
            "label": ws.cell(row_no, cols.index("label")).value,
            "created_at": now,
            "updated_at": now,
        }

        display_order = ws.cell(row_no, cols.index("display_order")).value
        try:
            fields["display_order"] = int(display_order) * order_coefficient
        except ValueError:
            pass

        rec = record.copy()
        rec["fields"] = fields
        data.append(rec)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Make indicator groups fixture from old site Excel export"
    )
    parser.add_argument("excel_file")
    parser.add_argument("--output", default="indicatorgroups.json")
    parser.add_argument("--order-coeff", type=int, default=1)
    args = parser.parse_args()
    make_fixture(args.excel_file, args.output, args.order_coeff)
