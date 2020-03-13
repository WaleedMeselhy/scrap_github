#!/usr/bin/env bash

set -o errexit
set -o pipefail

# set -o nounset
cmd="$@"

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi
if [ -z "$POSTGRES_PORT" ]; then
    export POSTGRES_PORT=5432
fi
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
function postgres_ready() {
    python <<END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

function escrapyd_ready() {
    response=$(curl --write-out %{http_code} --silent --output /dev/null $SCRAPYD_HOST)
    if [ $response -ge 200 ]; then
        return 0
    else
        return -1
    fi
}

until escrapyd_ready; do
    echo >&2 "Scrapyd is unavailable - sleeping"
    sleep 1
done
echo >&2 "Scrapyd is up - continuing..."

until postgres_ready; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing..."

if [ -z "$cmd" ]; then
    if [ "x$localdev" = "xtrue" ]; then
        exec python manage.py run -h 0.0.0.0
    else
        exec /app/gunicorn.sh
    fi
else
    exec $cmd
fi
