# Install Docker

Installation instructions with docker, assuming that the host machine setup is complete.

## Docker Setup
 
- Clone the repository, or just download the relevant files:
  - [.env.example](https://raw.githubusercontent.com/digital-agenda-data/digital-agenda/master/.env.example) 
  - [docker-compose.yml](https://raw.githubusercontent.com/digital-agenda-data/digital-agenda/master/docker-compose.yml) 
  - [docker-compose.override.example.yml](https://raw.githubusercontent.com/digital-agenda-data/digital-agenda/master/docker-compose.override.example.yml)
- Make sure docker and docker-compose-plugin is installed 
- Copy override example and adjust as necessary:
  ```shell
  cp docker-compose.override.example.yml docker-compose.override.yml  
  ```
- Copy env example and adjust as necessary. Most values will be set to working 
  defaults
  ```shell
  cp .env.example .env
  ```
- Start services
  ```shell
  docker compose up -d 
  ```
- Load initial fixtures
  ```shell
  docker compose exec app ./manage.py load_initial_fixtures
  ``` 
- Create a super user 
  ```shell
  docker compose exec app ./manage.py createsuperuser
  ```
- Import data from ESTAT  
  ```shell
  docker compose exec app ./manage.py estat_import
  ```
  
## Updating 

- Update the git repo
- Restart services
  ```shell
  docker compose up -d
  ```