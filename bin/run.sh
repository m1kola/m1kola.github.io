#! /bin/sh

set -e

# Run migrations
python manage.py migrate --noinput

# Run CMD
exec "$@"
