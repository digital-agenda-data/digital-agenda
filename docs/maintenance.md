# Maintenance

## Clearing caches 

Caches are automatically invalidated when any model instance (from apps where the `auto_clear_cache` flag is SET) changes using `post_save` Django signals. 

There may however be scenarios where manually clearing the cache is required. (E.g. after new releases) This can be manually accomplished by running the following command:

```shell
python manage.py clear_cache
```