# Maintenance

## Clearing caches 

Caches are automatically invalidated when:
- the application is started/restarted
- any model instance changes (only from apps where the `auto_clear_cache` flag is SET). 

There may however be scenarios where manually clearing the cache is required. This can be manually accomplished by running the following command:

```shell
python manage.py clear_cache
```

To disable caching altogether set the env variable to 0:

```dotenv
CACHE_TIMEOUT=0
```