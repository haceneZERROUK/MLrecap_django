#!/bin/bash
set -e  

cd /django_app/niab 
echo "Démarrage du script d'entrypoint"
echo "Répertoire actuel: $(pwd)"

echo "########## migrations ##########"
python manage.py makemigrations
python manage.py migrate

echo "########## collecting static files ##########"
python manage.py collectstatic --noinput --clear

echo "########## Création de l'utilisateur admin ##########"
python ./create_admin.py

echo "########## Exécution du chargement initial des données ##########"
python ./data_load_once.py

echo "########## Démarrage du planificateur en arrière-plan ##########"
mkdir -p /var/log || true
python ./data_scheduler.py > /var/log/scheduler.log 2>&1 &

echo "########## Starting Gunicorn ##########"
exec gunicorn niab.wsgi:application --bind 0.0.0.0:8800 --workers 3 --log-level debug
# exec gunicorn niab.wsgi:application --bind 0.0.0.0:8800 --workers=1 --log-level debug --capture-output

