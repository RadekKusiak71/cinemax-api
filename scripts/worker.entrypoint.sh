#!/bin/bash

set -e

IS_DEBUG=${DJANGO_DEBUG:-"False"}

if [ "$IS_DEBUG" = "True" ]; then
  echo "Running celery worker in debug mode..."
  celery -A config worker --loglevel=debug
else
  echo "Running in production mode..."
  celery -A config worker --loglevel=info
fi