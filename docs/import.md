## Eurostat data import

### Triggering import config

Import can be triggered via de Django admin interface. With one or more config selected choose the "import" action from the dropdown above the table and click on "Go". The tasks are executed asynchronously and the "status" field will show the status of the task, and can be:

 - Queued, task is still waiting for a worker to run it
 - Running, task is currently being executed by a worker
 - Completed, task has been executed and finished successfully; the timestamp of completion is saved in "Last Import Time"
 - (error details) in case of any errors the error details are instead saved in this field

Imports can also be triggered via cmd line using the `estat_import` management command. Destructive actions will require user interactive confirmation unless the `--no-input` argument is given. Example:

```shell
[digital-agenda@digital-agenda-data ~]$ docker compose exec app ./manage.py estat_import --code educ_uoe_grad03 --delete-existing --force-download
Warning! This will remove 654 facts from 1 import configurations. Continue? [Y/n] Y
[2023-01-18 14:05:22] INFO digital_agenda.apps.estat.tasks: Processing config: <ImportConfig: educ_uoe_grad03 (1)> (tasks.py:15)
[2023-01-18 14:05:22] INFO digital_agenda.apps.estat.tasks: Deleted Facts: (654, {'core.Fact': 654}) (tasks.py:23)
[2023-01-18 14:05:22] INFO digital_agenda.apps.estat.estat_import: Downloading from: https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_grad03?compressed=true&format=JSON&lang=en (estat_import.py:78)
[2023-01-18 14:05:23] INFO digital_agenda.apps.estat.estat_import: Decompressing JSON: educ_uoe_grad03 (estat_import.py:85)
[2023-01-18 14:05:23] INFO digital_agenda.apps.estat.estat_import: Processing dataset: /.fs/estat/educ_uoe_grad03.json (estat_import.py:65)
[2023-01-18 14:05:25] INFO digital_agenda.apps.estat.estat_import: Importing with <ImportConfig: educ_uoe_grad03 (1)> (estat_import.py:267)
[2023-01-18 14:05:40] INFO digital_agenda.apps.estat.estat_import: Batch processed <ImportConfig: educ_uoe_grad03 (1)>; fact objs created 654 / 1533168 (estat_import.py:272)
[2023-01-18 14:05:40] INFO digital_agenda.apps.estat.estat_import: Assigning indicator datasource (estat_import.py:279)
[2023-01-18 14:05:40] INFO digital_agenda.apps.core.cache: Clearing cache 'default' (cache.py:17)
```

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

