## Eurostat data import

### Triggering import config

Import can be triggered via de Django admin interface. With one or more config selected, choose the "import" action from
the dropdown above the table and click on "Go". The tasks are executed asynchronously and the "latest task" field will
show the status of the last import run. Clicking on it will provide more details
such as import logs. On failure, the `errors` JSON field is populated with the relevant details - e.g. the unknown
dimension codes encountered in the file's data.

Using the "Delete existing facts and trigger import" option instead will first delete any facts that are linked to the
import config and as well as force redownloading the dataset from ESTAT instead of using a locally cached version, if
that was available in the first place.

The cached dataset is automatically checked if stale or not before use in an import by validating the local data with
the metadata API from ESTAT.
If the cache is stale, the new version will be downloaded before the import.

Details for all historical runs can be found in the "Import config results" section of the admin.

---

Imports can also be triggered via cmd line using the `estat_import` management command. Destructive actions will require
user interactive confirmation unless the `--no-input` argument is given. Example:

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

Imports are started by creating a new record in the "Upload data from file" admin site section.
Once a file is uploaded and the record is saved, the import task will run asynchronously, and update the record status
when completed. On failure, the `errors` JSON field is populated with the relevant details - e.g. the unknown
dimension codes encountered in the file's data.

Historical runs for each import can be found under "Upload data from file results" with all the logs and errors for each
run.

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

## Updating data

Whenever data is imported (either via file upload or ESTAT import), any old fact value that already existed with the
same unique key will be updated. The fact will also be linked to the new file/import and unliked from the old
file/import it was imported from.

The unique key consists of the following columns:

- indicator
- breakdown
- unit
- country
- period

Values update on duplicate key:

- value
- flags
- import_file
- import_config

## Replacing data

If a full replacement of data is required (either via file upload or ESTAT import), you can either:

- modify the existing "Upload data from file" entry, by changing the "file" field and uploading a new file in its place
- modify the existing "Import Config" entry, by changing the filters/mapping/dimensions/etc.
- select the checkbox in the list view for the updated entry
- select "Delete existing facts and trigger import" from the dropdown above and click on GO

This will effectively replace all old data with the new version, including deleting any old entries that are no longer
present in the new version.

## Purge data

To delete all facts related to a chart group:

- Navigate to the chart group list in the admin
- Select the checkboxes next to the chart groups you want data deleted for
- Select the "Purge data" action in the top dropdown and hit go

An intermediate confirmation page will allow you to review what will be deleted before confirming and proceeding with
the removal.

**Warning!** Chart groups can have overlapping facts. So deleting data using this method MAY affect other chart groups
and have unintended consequences.

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
In both cases, warnings are issued for unknown references, and those association records are **not** included in the
links fixture.

