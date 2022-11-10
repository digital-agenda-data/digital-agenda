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
- Frontend:
    - [vue](https://vuejs.org/guide/introduction.html)
    - [pinia](https://pinia.vuejs.org/)
    - [vue-router](https://router.vuejs.org/)
    - [vite](https://vitejs.dev/)
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
  pip install -c requirements/constraints.txt -r requirements/base.txt -r requirements/dev.txt
  ```
- Resolve any dependency problems, if any
- Freeze the new constraints
  ```bash
  pip freeze > requirements/constraints.txt
  ``` 