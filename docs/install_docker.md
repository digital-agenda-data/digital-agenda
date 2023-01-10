# Install Docker

This is the backend for the Digital Agenda **Data Visualisation Tool**.

## Docker Setup
 
- Clone the repository
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
- Build and start services
  ```shell
  docker compose build --pull
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
  
## Updating 

- Update the git repo
- Rebuild and restart services
  ```shell
  docker compose build --pull
  docker compose up -d
  ```