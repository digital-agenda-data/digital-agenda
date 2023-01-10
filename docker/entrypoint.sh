#!/usr/bin/env bash

set -e

wait-for-it "$REDIS_HOST":"${REDIS_POST:-6379}" --timeout=60
wait-for-it "$POSTGRES_HOST":"${POSTGRES_PORT:-5432}" --timeout=60

if [ "$DJANGO_MIGRATE" = "yes" ]; then
    ./manage.py migrate --noinput
    ./manage.py collectstatic --noinput
fi

exec "$@"

