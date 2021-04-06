from celery import Celery
from decouple import config


def get_celery_app():
    ENVIRONMENT = config("ENVIRONMENT")
    if ENVIRONMENT == "local":
        app = Celery('project_manager')
    else:
        app = Celery('project_manager', broker="pyamqp://rabbitmq:5672")

    return app
