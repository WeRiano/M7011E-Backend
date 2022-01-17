#!/bin/sh

set -e

python manage.py wait_for_db
#python manage.py collectstatic --noinput
python manage.py migrate

#uwsgi --ini backend_uwsgi.ini
uwsgi --http :8000 --master --module backend.wsgi
