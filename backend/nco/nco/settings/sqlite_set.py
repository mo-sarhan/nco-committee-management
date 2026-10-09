from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'oracledb':{
        'ENGINE':'django.db.backends.oracle',
        'NAME':'connection string here',
        'USER':'user',
        'PASSWORD':'Password',
        'HOST':'host'
    },
}

MANAGED_MIGRATIONS = True
DEBUG = True
