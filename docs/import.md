## Eurostat data import

### Bulk Metadata

Import Eurostat bulk metadata for each source dataset, e.g.:

```shell
./manage.py estat-import-bulk-meta isoc_bde15dec \
--indicator=indic_is \
--breakdown=sizen_r2 \
--unit=unit \
--country=geo \
--period=time \
--delete-existing
```

Eurostat dataset dimension values are imported in a disabled state, 
to avoid accidentally loading large amounts of unwanted facts.
Enable the appropriate values using the command:

```shell
./manage.py estat-enable-dim-values <JSON file>
```

where the input file has a structure mapping dataset, dimension and values, e.g.:

```json
{
  "isoc_bde15dec": {
    "indic_is": [
      "e_crman",
      "e_ebuy"
    ]
  },
  "isoc_bde15ee": {
    "indic_is": [
      "e_igov",
      "e_igov2",
      "e_igov3",
      "e_igovpr",
      "e_igov2pr",
      "e_igovrt",
      "e_igov2rt"
    ]
  }
}
```

See the `examples` directory for sample input file.
Note that some indicators are present in multiple datasets. Avoid enabling an indicator 
value multiple times - while this will not be a problem during the bulk data import, it
can cause data integrity problems during the final data processing (see the dashboard 
queries section below).

### Bulk data

Once the metadata is in place, load the bulk metadata for each dataset, e.g.:

```shell
./manage.py estat-import-bulk-data isoc_bde15dec
```

### Dashboard Queries

Imported bulk data is processed into the final reporting format using SQL queries defined 
in the Dashboard.

#### Database preparation

Create a read-only user for dashboard usage, matching the values 
in the settings items `POSTGRES_DASHBOARD_USER` & `POSTGRES_DASHBOARD_PASSWORD`:

```postgresql
CREATE ROLE da_ro WITH
    LOGIN
    NOSUPERUSER
    INHERIT
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    PASSWORD 'da_ro';
```

Allow the read-only user to read the bulk tables:

```postgresql
GRANT SELECT ON TABLE
    public.estat_datasets,
    public.estat_dimensions,
    public.estat_dim_values,
    public.estat_facts
TO da_ro;
```

Note: non-superuser application users must belong to the `Dashboard` group 
(pre-created during migrations) to be able to view and edit dashboards and queries.
The dashboard app is available at the `/dashboard/` URL.

Add dashboards and SQL queries for importing bulk facts into the core tables - an example 
query is available in `examples/ENT2_after_2009.sql`. Note that while each dashboard supports 
multiple queries, only the first is used during the final import stage, by specifying the 
dashboard's slug as the parameter:

```shell
./manage.py import-with-query ent2_after_2009
```

Be aware that core facts must have unique indicator/breakdown/unit/country/period combinations. 
Consequently, dashboard queries must either enforce this, or avoid data duplication, e.g. from 
indicators that are present in multiple datasets. Otherwise, the `import-with-query` command will 
terminate with data integrity errors, and the import must be re-run after fixing the query.


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

