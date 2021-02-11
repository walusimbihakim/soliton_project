#Grab the latest alpine image
FROM alpine:latest

# Install python and pip
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


RUN python3 -m pip install --upgrade wheel

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pillow
RUN pip install Django==2.2.2
RUN pip install django-crispy-forms==1.9.2
RUN pip install django-javascript-settings
RUN pip install django-model-utils
RUN pip install gunicorn
RUN pip install whitenoise==5.2.0

COPY . /code/

# FOR HEROKU
RUN python3 manage.py migrate --noinput
# collect static files
RUN python3 manage.py collectstatic --noinput

# Run the image as a non-root user
RUN adduser -D myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --bind 0.0.0.0:$PORT project_manager.wsgi


