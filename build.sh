#!/bin/bash

echo "Building project packages..."
pip install -r requirements.txt

echo "Generating database URL..."
python program.py

echo "Migrating database..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Removing inessential files..."
rm database.txt program.py README.md
