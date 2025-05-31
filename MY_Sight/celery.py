import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MY_Sight.settings')

app = Celery('MY_Sight')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
