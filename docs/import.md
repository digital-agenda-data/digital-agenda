## Eurostat data import

XXX TODO

## Excel Data Import

Facts can be loaded from Excel files (`.xls` and `.xlsx` formats supported).

Imports are started by creating a new record in the "Data file imports" admin site section.
Once a file is uploaded and the record is saved, the import task will run asynchronously, and update the record status when completed.
On failure, the `errors` JSON field is populated with the relevant details - e.g. the unknown dimension codes encountered in the file's data.

Data structure requirements:
- data is on the first sheet
- data starts on second row (header row is skipped, contents are not relevant)
- columns order is:
  - year
  - country	
  - indicator (variable)	
  - breakdown	
  - unit	
  - value	
  - flag(s)


## Creating fixtures

Alternative fixtures can be produced from Excel exports of code lists from the previous version:
```shell
python scripts/mk_data_sources_fixture.py source.xls
python scripts/mk_units_fixture.py unit-measure.xls
python scripts/mk_indicator_groups_fixture.py indicator-group.xls
python scripts/mk_indicators_fixture.py indicator.xls --groups-excel-file=indicator-group.xls --sources-excel-file=source.xls
python scripts/mk_breakdown_groups_fixture.py breakdown-group.xls 
python scripts/mk_breakdowns_fixture.py breakdown.xls --groups-excel-file=breakdown-group.xls
```
The scripts for the indicators and breakdowns fixtures also produce the "links" fixtures with their respective groups.
For indicators, integrity checks can be performed against the indicator groups and data sources Excel files. 
For breakdowns, validation of the group can be done versus the breakdown groups Excel file.  
In both cases, warnings are issued for unknown references, and those association records are **not** included in the links fixture.

