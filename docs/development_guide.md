# Development guide

## Style guide

- The backend code uses the [black style guide](https://black.readthedocs.io/en/stable/) for automatic linting.
- The frontend code uses ES lint and prettier. This can be integrated into your IDE or manually run with:
  ```bash
  cd frontend && npm run lint
  ```
  
## Starting points

- API documentation can be explored with [redocs](http://localhost:8000/api/v1/schema/redoc/) 
  or [swagger](http://localhost:8000/api/v1/schema/swagger-ui/#/) while running locally 
- API calls can be made from the frontend using the libray in [lib/api.js](../frontend/src/lib/api.js)
- Backend:
    - [django](https://docs.djangoproject.com//)
    - [django-rest-framework](https://www.django-rest-framework.org/)
    - [celery](https://docs.celeryq.dev/en/stable/)
    - [pytest](https://docs.pytest.org/)
- Frontend:
    - [vue](https://vuejs.org/guide/introduction.html)
    - [vueuse](https://vueuse.org/functions.html)
    - [pinia](https://pinia.vuejs.org/)
    - [vue-router](https://router.vuejs.org/)
    - [vite](https://vitejs.dev/)
    - [Cypress testing](https://docs.cypress.io/)
    - [Europa Component Library](https://ec.europa.eu/component-library/)

## Adding a new backend dependency

To add a new dependency:

- Add it to either [base.txt](../requirements/base.txt) if the dependency needs to be run in production
  or [dev.txt](../requirements/dev.txt) if the dependency is only needed for developing. 
- Create a new virtualenv and activate it 
  ```bash
  virtualenv .venv && source .venv/bin/activate
  ```
- Install all dependencies
  ```bash
  pip install -r requirements/dev.txt -r requirements/prod.txt -c requirements/constraints.txt
  ```
- Resolve any dependency problems, if any
- Freeze the new constraints
  ```bash
  pip freeze > requirements/constraints.txt
  ``` 
  
## ECL Viewport Breakpoints

See more details here: https://ec.europa.eu/component-library/ec/utilities/layout/grid/

|     | Name        | Min Viewport Width |
|-----|-------------|--------------------|
| xs  | Extra small | ≥ 0px              |
| s   | Small       | ≥ 480px            |
| m   | Medium      | ≥ 768px            |
| l   | Large       | ≥ 996px            |
| xl  | Extra large | ≥ 1140px           |

## Previewing production build locally

Checking certain aspects of the app (like bundle chunking and sizes) requires previewing 
a production build. To do so follow these steps:

- Create an env config file in the frontend dir to point the API host at the local 
  backend server:
  ```shell
  $ cat frontend/.env.local 
  VITE_APP_API_HOST=localhost:8000
  ```
- Build frontend for prod
  ```shell
  cd frontend/
  npm run build
  ```
- A file will be generated with some bundle stats, that can be checked if needed:
  ```shell
  bundle.stats.html
  ```
- Use the preview script to serve the bundle locally:
  ```shell
  npm run preview
  ```