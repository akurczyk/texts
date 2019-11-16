#!/bin/sh

docker-compose -f docker-compose.k8s.yml exec django python manage.py collectstatic --no-input
docker-compose -f docker-compose.k8s.yml exec django python manage.py flush --no-input
docker-compose -f docker-compose.k8s.yml exec django python manage.py migrate --no-input
docker-compose -f docker-compose.k8s.yml exec django python manage.py createsuperuser
