from __future__ import absolute_import
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')


RUN_DOCKERIZED = os.environ.get('RUN_DOCKERIZED')

REDIS_HOST = 'redis' if RUN_DOCKERIZED else '127.0.0.1'
REDIS_HOST = '0.0.0.0'

CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Bucharest'
    broker_url = CELERY_RESULT_BACKEND
    backend_url = CELERY_RESULT_BACKEND
    imports = ('main.tasks',)


app = Celery(namespace='inventory')
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()