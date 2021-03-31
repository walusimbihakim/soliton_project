import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
app = Celery('project_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'add-every-wednesday-at-9-30': {
        'task': 'projects.tasks.create_wage_bill',
        'schedule':  crontab(hour=9, minute=30, day_of_week=3),
    },
}



