
from .base import *
import os


import django.db.backends.postgresql
DATABASES = {
    'default':{
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
}

MANAGED_MIGRATIONS = True

ALLOWED_HOSTS = ['localhost','www.afrad.mil.eg','afrad.mil.eg','afrad.oma.mil.eg']

CORS_ALLOWED_ORIGINS = [
    'https://www.afrad.mil.eg',
]
CSRF_TRUSTED_ORIGINS = ['https://www.afrad.mil.eg']

STATIC_URL = '/static/'
STATIC_ROOT =  os.path.join(BASE_DIR, 'static') 
MEDIA_URL =  '/images/'
# MEDIA_ROOT = r'T:\app_photo\media'





# for (HSTS)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')
# SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# for (XCTO)
# SECURE_CONTENT_TYPE_NOSNIFF = True


# for cookies
# SESSION_COOKIES_HTTPONLY = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True


DEBUG = True
# CORS_ALLOW_ALL_ORIGINS=True
