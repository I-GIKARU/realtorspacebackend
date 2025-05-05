#!/usr/bin/env bash
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files with specific settings
DJANGO_SETTINGS_MODULE=core.settings_collect python manage.py collectstatic --no-input --clear

# Run database migrations
python manage.py migrate
