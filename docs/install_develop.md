# Installing for development

**WARNING! DO NOT USE THIS DEPLOYMENT IN A PRODUCTION ENVIRONMENT!**

This document describes installation steps required to install locally for development.

## Preparing environment

- Install nodejs (>=16)
- Install python and python-dev (>=3.10)
- Install and start postgresql (>=14)
- Install and start redis (>=6)
- Install required packages for building dependencies:
  ```
  gettext build-essential gcc
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
  cp .env.example .env
  ```
- Install dependencies
  ```shell
  pip install -c requirements/constraints.txt -r requirements/dev.txt 
  ```
- Run migrations
  ```shell
  python manage.py migrate
  ```
- Create superuser
  ```shell
  python manage.py createsuperuser
  ```
- Load initial fixtures
  ```shell
  python manage.py load_initial_fixtures
  ```

## Running the application

- Start the backend with hot-reload
  ```shell
  python manage.py runserver
  ```
- Start worker *(**NOTE** Celery does not have hot-reload, changes to the code will require a restart)*
  ```shell
  celery -A digital_agenda worker -c 1 -l debug
  ```