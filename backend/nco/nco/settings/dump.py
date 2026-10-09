
from .base import *

DATABASES = {
    'postgre':{
        'ENGINE':'django.db.backends.postgresql',
        'HOST':'localhost',
        'PORT':'5432',
        'NAME': 'nco',
        'USER':'nco',
        'PASSWORD':'P@ssw0rd'

    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
