import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_platform.settings')

app = Celery('edu_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# ✅ Расписание задач Celery Beat
app.conf.beat_schedule = {
    'block-inactive-users-every-day': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # каждый день в 00:00
    },
}
