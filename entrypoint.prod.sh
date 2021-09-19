#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --no-input
#echo "from django.contrib.auth.models import User" > createadmin.py
#echo "User.objects.create_superuser('admin', 'admin@admin.admin', 'admin')" >> createadmin.py
#python manage.py shell < createadmin.py

exec "$@"