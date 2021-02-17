#Grab the latest alpine image
FROM alpine:latest
# Install python and pip
ENV SECRET_KEY 0d1*j&^q381!@3^^4htw!n-1p!yxxy93s3^2exrw7%4bf_!hcf
ENV DEBUG True
ENV ALLOWED_HOSTS .localhost, .herokuapp.com, 127.0.0.1
ENV REDIS_URL redis://:p5a881ed3de5e49ff35a4ed3f7707c9f9095e35332405e81afff1d28cf1c24337@ec2-52-22-235-152.compute-1.amazonaws.com:13569
ENV CELERY_RESULT_BACKEND django-db
ENV CELERY_ACCEPT_CONTENT json
ENV CELERY_TASK_SERIALIZER json
ENV CELERY_RESULT_SERIALIZER json
ENV CELERY_TIMEZONE Africa/Kampala

RUN apk add --no-cache --update python3 py3-pip bash
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
WORKDIR /code
COPY requirements.txt /code/
RUN pip install Django==2.2.2
RUN pip install django-crispy-forms==1.9.2
RUN pip install django-javascript-settings
RUN pip install django-model-utils
RUN pip install gunicorn
RUN pip install whitenoise==5.2.0
RUN pip install celery
RUN pip install redis
RUN pip install python-decouple
RUN pip install django-celery-results
RUN pip install django-celery-beat

COPY . /code/
# FOR HEROKU
RUN python3 manage.py migrate --noinput
# collect static files
RUN python3 manage.py collectstatic --noinput
# Run the image as a non-root user
USER root

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --bind 0.0.0.0:$PORT project_manager.wsgi

