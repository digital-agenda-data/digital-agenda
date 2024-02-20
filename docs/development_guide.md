# Development guide

## Style guide

- The backend code uses the [black style guide](https://black.readthedocs.io/en/stable/) for automatic linting. Can
  be integrated into your IDE or manually run with:
  ```bash
  black --extend-exclude=migrations digital_agenda/
  ```
- The frontend code uses ES lint and prettier. This can be integrated into your IDE or manually run with:
  ```bash
  cd frontend && npm run lint
  ```
  
A workflow is integrated into GitHub action to check that any code push has been first processed with the project
settings. See [code style workflow](https://github.com/digital-agenda-data/digital-agenda/actions/workflows/lint.yml)
  
## Starting points

- API documentation can be explored with [redocs](http://localhost:8000/api/v1/schema/redoc/) 
  or [swagger](http://localhost:8000/api/v1/schema/swagger-ui/#/) while running locally 
- API calls can be made from the frontend using the axios instance from [lib/api.js](../frontend/src/lib/api.js)
- Backend:
    - [django](https://docs.djangoproject.com//)
    - [django-rest-framework](https://www.django-rest-framework.org/)
    - [django-task](https://github.com/morlandi/django-task)
    - [pytest](https://docs.pytest.org/)
- Frontend:
    - [vue](https://vuejs.org/guide/introduction.html)
    - [vueuse](https://vueuse.org/functions.html)
    - [pinia](https://pinia.vuejs.org/)
    - [vue-router](https://router.vuejs.org/)
    - [vite](https://vitejs.dev/)
    - [Cypress testing](https://docs.cypress.io/)
    - [Europa Component Library](https://ec.europa.eu/component-library/)
- [European Commission WebTools](https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Webtools+documentation+-+Homepage), 
  documentation requires an account to view (with 2FA active) 
    - [Global banner](https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Global+banner) 
    - [Cookie Consent Banner](https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Cookie+Consent+Kit+Banner)
    - [Europa Analytics](https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Europa+Analytics)
    - ~~[Share buttons](https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Social+bookmarking+and+networking)~~
      (Removed for now as it only works for `*.europa.eu` domains)
- [Eurostat](https://ec.europa.eu/eurostat)
  - [Data download API](https://wikis.ec.europa.eu/display/EUROSTATHELP/API+SDMX+2.1+-+data+query)
- Misc:
    - EU Login - No documentation available; however it is a CAS server, so see [django-cas-ng](https://djangocas.dev/docs/latest/) instead.    
    - [EU Captcha](https://github.com/pwc-technology-be/EU-CAPTCHA)

## Testing data

Minimal data used for testing can be added with the "seed_db" management command.

```shell
./manage.py seed_db
```

This will:

 - remove ALL existing data
 - creates an admin user with credentials: 
   - user: `admin@example.com`
   - password: `admin`
 - load the base fixtures (countries/indicators/breakdowns/etc.)
 - load a small subset of data for DESI directly from fixtures
 - creates a few small ESTAT import configs for "Key Indicators" and imports the data
 - adds images for all chart groups

This command is required to run the [E2E tests](./tests.md#running-e2e-tests)

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
a production build. To do so, follow these steps:

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
- Use the preview script to serve the bundle locally:
  ```shell
  npm run preview
  ```