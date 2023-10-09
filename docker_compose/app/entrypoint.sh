#!/bin/sh
set -e

echo Starting postgres
until PGPASSWORD=$DB_PASSWORD psql -h db -U app -d movies_database -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  echo $DB_USER
  echo $DB_PASSWORD
  sleep 1
done
echo PostgreSQL started

echo Creating DB structure
PGPASSWORD=$DB_PASSWORD psql -h db -U app -d movies_database -f movies_database.ddl

echo Run migrations
export DB_HOST=db

python manage.py migrate --fake sessions zero
python manage.py migrate --fake movies zero
python manage.py migrate --fake-initial
python manage.py migrate
python manage.py makemigrations

python ./sqlite_to_postgres/load_data.py 

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi
    
uwsgi --ini uwsgi.ini

exec "$@"
