#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=Passer@123
python manage.py createsuperuser \
    --no-input \
    --username admin2 \
    --email admin@test.com