import argparse
import json

import xlrd


def make_fixture(
    excel_file,
    groups_excel_file,
    sources_excel_file,
    indicators_output_path,
    group_links_output_path,
    order_coefficient,
):
    cols = (
        "code",
        "label",
        "alt_label",
        "definition",
        "note",
        "group",
        "display_order",
        "data_source",
    )

    data = []
    record = {"model": "core.indicator", "fields": None}

    group_link_data = []
    group_link_record = {"model": "core.indicatorgrouplink", "fields": None}

    group_codes = []
    if groups_excel_file is not None:
        wb = xlrd.open_workbook(groups_excel_file)
        ws = wb.sheet_by_index(0)
        group_codes = set([v.strip().lower() for v in ws.col_values(0, 1)])

    data_source_codes = []
    if sources_excel_file is not None:
        wb = xlrd.open_workbook(sources_excel_file)
        ws = wb.sheet_by_index(0)
        data_source_codes = set([v.strip().lower() for v in ws.col_values(0, 1)])

    wb = xlrd.open_workbook(excel_file)
    ws = wb.sheet_by_index(0)
    for row_no in range(1, ws.nrows):
        code = ws.cell(row_no, 0).value.strip().lower()
        if not code:
            break

        fields = {
            "code": code,
            "label": ws.cell(row_no, cols.index("label")).value,
        }

        optional_fields = {
            "alt_label": ws.cell(row_no, cols.index("alt_label")).value.strip(),
            "definition": ws.cell(row_no, cols.index("definition")).value.strip(),
            "note": ws.cell(row_no, cols.index("note")).value.strip(),
        }

        fields.update({k: v for k, v in optional_fields.items() if v})

        data_source = ws.cell(row_no, cols.index("data_source")).value.strip().lower()
        if data_source:
            if data_source_codes and data_source not in data_source_codes:
                print(
                    f"Unknown data source {data_source} for indicator {code} - skipping association."
                )
            else:
                fields["data_source"] = [data_source]

        rec = record.copy()
        rec["fields"] = fields
        data.append(rec)

        group_link_rec = None
        group = ws.cell(row_no, cols.index("group")).value.strip().lower()
        if group:
            if group_codes and group not in group_codes:
                print(
                    f"Unknown group {group} for breakdown {code} - skipping group association."
                )
            else:
                group_link_rec = group_link_record.copy()
                group_link_rec["fields"] = {"indicator": [code], "group": [group]}
                try:
                    display_order = (
                        int(ws.cell(row_no, cols.index("display_order")).value)
                        * order_coefficient
                    )
                    group_link_rec["fields"]["display_order"] = display_order
                except ValueError:
                    pass

        if group_link_rec is not None:
            group_link_data.append(group_link_rec)

    with open(indicators_output_path, "w") as f:
        json.dump(data, f, indent=2)

    with open(group_links_output_path, "w") as f:
        json.dump(group_link_data, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Make indicators and indicatorgrouplinks fixtures from old site indicators Excel export"
    )
    parser.add_argument("excel_file")
    parser.add_argument("--indicators-output", default="indicators.json")
    parser.add_argument("--group-links-output", default="indicatorgrouplinks.json")
    parser.add_argument("--order-coeff", type=int, default=1)
    parser.add_argument(
        "--groups-excel-file",
        help="Indicator groups Excel export file - used for integrity checks.",
    )
    parser.add_argument(
        "--sources-excel-file",
        help="Sources Excel export file - used for integrity checks.",
    )
    args = parser.parse_args()
    make_fixture(
        args.excel_file,
        args.groups_excel_file,
        args.sources_excel_file,
        args.indicators_output,
        args.group_links_output,
        args.order_coeff,
    )
