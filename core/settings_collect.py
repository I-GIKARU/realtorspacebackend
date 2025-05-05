"""
Temporary settings module for static file collection.
This imports all settings from the main settings module but overrides 
the static files storage to use Django's default.
"""

from core.settings import *

# Override STATICFILES_STORAGE to use Django's default
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Ensure DEBUG is True for development
DEBUG = True

# Make sure STATIC_ROOT and STATICFILES_DIRS are properly referenced
# These should be the same as in the main settings.py
print(f"Using STATIC_ROOT: {STATIC_ROOT}")
print(f"Using STATICFILES_DIRS: {STATICFILES_DIRS}")

