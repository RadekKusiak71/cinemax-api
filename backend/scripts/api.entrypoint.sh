#!/bin/bash

set -e

DJANGO_DEBUG=${DJANGO_DEBUG:-"False"}

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py create_admin_account

if [ "$DJANGO_DEBUG" = "True" ]; then
    echo "Running in DEBUG mode"
    gunicorn config.wsgi:application --bind 0.0.0.0:80 --reload --workers 1 --log-level=debug
else
    echo "Running in PRODUCTION mode"
    gunicorn config.wsgi:application --bind 0.0.0.0:80 --workers 3 --log-level=info
fi