#!/usr/bin/env bash
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collect_static_fixed --clear --no-input
# Run database migrations
python manage.py migrate
