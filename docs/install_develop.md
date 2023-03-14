# Installing for development

**WARNING! DO NOT USE THIS DEPLOYMENT IN A PRODUCTION ENVIRONMENT!**

This document describes installation steps required to install locally for development.

## Preparing environment

- Install nodejs (>=18)
- Install python and python-dev (>=3.11)
- Install and start postgresql (>=14)
- Install and start redis (>=6)
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
- Create superuser
  ```shell
  ./manage.py createsuperuser
  ```
- Load initial fixtures
  ```shell
  ./manage.py load_initial_fixtures
  ```
- _(optional)_ Import data from ESTAT
  ```shell
  ./manage.py estat_import
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
