#!/bin/sh

set -e

echo "Waiting for database..."
# Simple wait loop for DB (optional, but robust)
# In production, you might rely on restart policies or specialized wait scripts.

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
