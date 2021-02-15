FROM registry.heroku.com/sol-project-docker/web:latest
WORKDIR /code

CMD celery -A project_manager worker -l INFO
