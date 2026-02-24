#!/bin/bash
# Build script for Render.com
# Run migrations and collect static files
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
