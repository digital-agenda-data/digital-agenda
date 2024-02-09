# Installing for development

**WARNING! DO NOT USE THIS DEPLOYMENT IN A PRODUCTION ENVIRONMENT!**

This document describes installation steps required to install locally for development.

## Preparing environment

- Install nodejs (>=20)
- Install python and python-dev (>=3.12)
- Install and start postgresql (>=14)
- Install and start redis (>=7)
- Install required packages for building dependencies:
  ```
  gettext build-essential gcc libmagic1
  ```
- Create a postgresql database and user:
  ```shell
  sudo -u postgres createuser -Pds da && sudo -u postgres createdb da
  ``` 
- _(Recommended)_ create and activate a python virtualenv
- Clone this repository

## Installing Backend for development

- Configure local settings, starting from the dev example
  ```shell
  cp .env.develop.example .env
  ```
- Install dependencies
  ```shell
  pip install -c requirements/constraints.txt -r requirements/dev.txt 
  ```
- Run migrations
  ```shell
  ./manage.py migrate
  ```
- Add some testing data to the DB (see [development guide](./development_guide.md#testing-data) for details on what this
  includes):
  ```shell
  ./manage.py seed_db
  ```

## Installing Frontend for development

- Change directory to the frontend directory
  ```shell
  cd frontend
  ```
- Install dependencies
  ```shell
  npm install
  ```

## Running the application

- Start the backend with hot-reload
  ```shell
  ./manage.py runserver
  ```
- Start the frontend with hot-reload (from frontend directory)
  ```shell
  npm run dev
  ```  
- _(optional)_ Start worker. _**NOTE** Worker does not have hot-reload, changes to the code will require a restart_
  ```shell
  ./manage.py rqworker
  ```
- Check frontend is running correctly at http://localhost:8080
- Check backend is running correctly at http://localhost:8000 and login with credentials:
    - user: `admin@example.com`
    - password: `admin`

## Updating the application

- Update the code with the latest version
- Update third-party packages required at runtime.
  ```shell
  pip install -c requirements/constraints.txt -r requirements/dev.txt
  ```
- Update frontend dependencies
  ```shell
  cd frontend && npm install 
  ```
- Run migrations:
  ```shell
  ./manage.py migrate
  ```

## Where to go from here?

See the and [tests guide](./tests.md) to run some the test suites locally. Afterward check
the [development guide](./development_guide.md) to help you get started.  