import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger.settings')

app = Celery('messenger')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'logging-cur-online-every-5-min': {
        'task': 'users.tasks.insert_information_about_cur_online',
        'schedule': crontab(minute='*/1'),
    }
}
