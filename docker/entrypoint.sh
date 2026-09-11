#!/bin/sh
set -e

echo "Waiting for database at ${DB_HOST:-localhost}:${DB_PORT:-5432}..."
until python - <<'PYEOF'
import os
import socket
import sys

host = os.environ.get("DB_HOST", "localhost")
port = int(os.environ.get("DB_PORT", "5432"))

try:
    with socket.create_connection((host, port), timeout=2):
        sys.exit(0)
except OSError:
    sys.exit(1)
PYEOF
do
    sleep 1
done
echo "Database is up."

python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

exec gunicorn cofig.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --access-logfile - \
    --error-logfile -
