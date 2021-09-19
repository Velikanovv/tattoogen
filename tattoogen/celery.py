import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tattoogen.settings')

app = Celery('tattoogen')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-old-sketches-every-day': {
        'task': 'core.tasks.delete_old_sketches',
        'schedule': crontab(hour='*/24'),
    },
}