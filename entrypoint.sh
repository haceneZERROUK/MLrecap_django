#!/bin/bash

set -e  

cd /django_app/niab 

echo "########## migrations ##########"
python manage.py makemigrations
python manage.py migrate

echo "########## collecting static files ##########"
python manage.py collectstatic --noinput --clear


# création de la bdd et grant access


echo "########## creating superuser ##########"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@email.com',
        password='admin',
        first_name='Admin',
        last_name='adm',
    )
EOF

python ../data_load_save.py

echo "########## Starting Gunicorn ##########"
exec gunicorn niab.wsgi:application --bind 0.0.0.0:8800 --workers 3 --log-level debug
# exec gunicorn niab.wsgi:application --bind 0.0.0.0:8800 --workers 3 --log-level debug --capture-output

