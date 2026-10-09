from .base import *

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MANAGED_MIGRATIONS = False
DEBUG = False
