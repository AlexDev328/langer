#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input
#TODO запуск сервера тут или в compose?
