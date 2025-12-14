#!/bin/bash

set -e

IS_DEBUG=${DJANGO_DEBUG:-"False"}

if [ "$IS_DEBUG" = "True" ]; then
  echo "Running celery beat in debug mode..."
  celery -A config beat -l DEBUG --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
  echo "Running in production mode..."
  celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
fi