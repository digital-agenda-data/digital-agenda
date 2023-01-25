# Running tests 

## Running backend tests

- To run the full suite, make sure you have everything [installed for dev](./install_develop.md) and run
  ```shell
  pytest
  ```
- To run with coverage
  ```shell
  pytest --cov
  ``` 
- To run a specific test suite
  ```shell
  pytest digital_agenda/apps/estat/tests/test_importer.py 
  ```
- To run a specific test case class
  ```shell
  pytest digital_agenda/apps/estat/tests/test_importer.py::TestImporterErrors
  ```
- To run a specific test case method
  ```shell
  pytest digital_agenda/apps/estat/tests/test_importer.py::TestImporterErrors::test_invalid_mapping_value
  ```

## Running E2E tests 

Prepare env:

- Clone repository locally
- Make sure that the backend **and** frontend are **running**. Either using [install for dev](./install_develop.md) or 
  [install with docker](./install_docker.md).
- Seed the database with data for the E2E tests. Only needs to be done once, but if you change anything in the DB you 
  _may need to run it again_. 
  ```shell
  ./manage.py seed_db
  # OR if running in docker
  docker compose exec app ./manage.py seed_db
  ```
- Install dev frontend dependencies:
  ```shell
  cd frontend
  npm install
  ```

Running options:

- Open interactive Cypress test runner and manually run specs from there 
  ```shell
  npm run test:open
  ```
- Run the FULL suite headless 
  ```shell
  npm run test
  ```
- Run single spec headless 
  ```shell
  npm run test -- -s cypress/e2e/chart.cy.js
  ```
