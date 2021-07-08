import os
from celery.schedules import crontab
from project_manager.celery_function import get_celery_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
app = get_celery_app()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'add-every-wednesday-at-9-30': {
        'task': 'projects.tasks.create_wage_bill',
        'schedule':  crontab(hour=12, minute=30, day_of_week=3),
    },
    'wage-sheets-reminder-every-tuesday': {
        'task': 'projects.tasks.wage_sheets_submission_reminder',
        'schedule':  crontab(hour=9, minute=30, day_of_week=2),
    },
}



