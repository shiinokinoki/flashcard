#!/bin/sh

docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser
