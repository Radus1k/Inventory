#!/bin/sh

python manage.py makemigrations accounts
python manage.py makemigrations dashboard
python manage.py makemigrations websites
python manage.py makemigrations main
python manage.py migrate accounts
python manage.py migrate dashboard
python manage.py migrate websites
python manage.py migrate main
python manage.py migrate


python manage.py runserver 0.0.0.0:8000


exec "$@"
