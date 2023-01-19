# Running tests 

## Running backend tests

- To run the full suite, make sure you have everything [installed for dev](./install_develop.md) and run
  ```shell ../
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
