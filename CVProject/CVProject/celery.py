import os
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='CVProject.settings')

app = Celery('CVProject')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
