#!/bin/bash

python manage.py makemigrations
python manage.py migrate
uvicorn --reload --host 0.0.0.0 --port 8000 config.asgi:application