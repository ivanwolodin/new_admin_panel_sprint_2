#!/bin/sh
set -e

echo "Starting postgres"
until PGPASSWORD=$DB_PASSWORD psql -h db -U app -d movies_database -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  echo $DB_USER
  echo $DB_PASSWORD
  sleep 1
done
echo "PostgreSQL started"

echo Creating DB structure
PGPASSWORD=$DB_PASSWORD psql -h db -U app -d movies_database -f movies_database.ddl

echo Run migrations
echo db
echo $(db)
export DB_HOST=db
python manage.py flush --no-input
python manage.py migrate

python ./sqlite_to_postgres/load_data.py 

exec "$@"
