#!/bin/sh
set -e

echo "Running entrypoint.sh"

python manage.py wait_for_db

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec "$@"
