FROM registry.heroku.com/sol-project-docker/web:latest
WORKDIR /code

CMD celery -A project_manager beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
