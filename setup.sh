#!/bin/sh

docker-compose exec django python manage.py collectstatic --no-input
docker-compose exec django python manage.py flush --no-input
docker-compose exec django python manage.py migrate --no-input
docker-compose exec django python manage.py createsuperuser
