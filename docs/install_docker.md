# Install Docker

This is the backend for the Digital Agenda **Data Visualisation Tool**.

## Docker Setup

Build the images:

```shell
docker/build.sh
```

Bring up the app and database:

```shell
export COMPOSE_FILE=docker/docker-compose.yml
export DOCKER_ENV_FILE=docker.env
docker-compose up -d
```

Drop into an app container shell, e.g.:

```shell
docker-compose exec app-http bash
```

to perform Django initialization routines:

```shell
django-admin migrate
django-admin collectstatic
django-admin createsuperuser
```

Note that `createsuperuser` can rely on envars `DJANGO_SUPERUSER_EMAIL` & `DJANGO_SUPERUSER_PASSWORD`, if available:
```shell
django-admin createsuperuser --noinput
```

## Initial metadata

The `core` app (`digital_agenda.apps.core`) provides fixtures for seeding:
- data sources
- indicator groups
- indicators
- breakdown groups
- breakdowns
- units of measure

To import these fixtures:

- Copy fixtures in the container:
  ```shell
  docker compose cp src/digital_agenda/apps/core/fixtures/ app-http:/fixtures/
  docker compose exec app-http bash
  cd fixtures/
  ```
- Run import command (order matters):
  ```shell
  django-admin loaddata \
    datasources \
    indicatorgroups \
    indicators \
    indicatorgrouplinks \
    breakdowngroups \
    breakdowns \
    breakdowngrouplinks \
    units
  ```
  
---

**XXX TODO** Missing steps for this to work with docker: 

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