#!/bin/bash

set -e
psql -h localhost -U app -d movies_database -f movies_database.ddl
service postgresql start
echo "Starting with db"
until psql -h localhost --username=$POSTGRES_USER $POSTGRES_DB -w &>/dev/null
do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# echo "Postgres is ready, creating schema..."
# sudo service postgresql start
# psql -h localhost -U app -d movies_database -f movies_database.ddl

exec "$@"