from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','nco.settings.production')



app = Celery('nco')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()