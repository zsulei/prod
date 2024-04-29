import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outletobuv_core.settings')

app = Celery('outletobuv_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'start_func_every_15_mins': {
        'task': 'products.tasks.start_func',
        'schedule': crontab(minute='*/15'),
    },
}
