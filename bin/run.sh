#! /bin/sh

set -e

# Run migrations
python manage.py migrate --noinput

# Run uWSGI
exec uwsgi --module=wsgi --processes=10 --http=:8080 --harakiri=20 --max-requests=5000 --master --vacuum "$@"
