#! /bin/sh

set -e

# Run migrations
python manage.py migrate --noinput

# Run uWSGI
exec uwsgi --ini uwsgi.ini "$@"
