#!/usr/bin/env sh
set -e
python ecommerce/manage.py migrate --noinput || true
exec "$@"
