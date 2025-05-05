"""
Temporary settings module for static file collection.
"""
import os
from pathlib import Path
from core.settings import *

# Force DEBUG to ensure static files are handled properly
DEBUG = True

# Use the most basic storage backend
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configure static files settings
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = 'static/'

# Make paths absolute
if os.environ.get('RENDER'):
    STATIC_ROOT = '/opt/render/project/src/staticfiles'
    STATICFILES_DIRS = ['/opt/render/project/src/static']
else:
    STATIC_ROOT = str(BASE_DIR / 'staticfiles')
    STATICFILES_DIRS = [str(BASE_DIR / 'static')]

# Remove all middleware that might interfere
MIDDLEWARE = [
    m for m in MIDDLEWARE 
    if not any(x in m.lower() for x in ['static', 'whitenoise', 'compress'])
]

# Reorder installed apps to ensure correct precedence
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'properties',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
]

# Print debug info
print(f"Using STATIC_ROOT: {STATIC_ROOT}")
print(f"Using STATICFILES_DIRS: {STATICFILES_DIRS}")
