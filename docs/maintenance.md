# Maintenance

## Disabling inactive accounts

Accounts are automatically disabled after a set period of inactivity according to the `USER_INACTIVE_DAYS` config value.
The script that disables accounts periodically can also be manually run if needed with different values. 
For example:

```shell
docker compose exec app ./manage.py disable_inactive_accounts --days=10
```


## Clearing caches 

Caches are automatically invalidated when:
- the application is started/restarted
- any model instance changes (only from apps where the `auto_clear_cache` flag is SET). 

There may, however, be scenarios where manually clearing the cache is required. 
This can be manually accomplished by running the following command:

```shell
docker compose exec app ./manage.py clear_cache
```

To disable caching altogether, set the env variable to 0:

```dotenv
CACHE_TIMEOUT=0
```