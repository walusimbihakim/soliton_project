FROM python:3.8.5-alpine

RUN pip install --upgrade pip
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt


RUN python3 manage.py collectstatic --no-input
RUN python manage.py migrate --no-input

#gunicorn project_manager.wsgi:application --bind 0.0.0.0:8000
CMD gunicorn project_manager.wsgi:application --bind 0.0.0.0:$PORT

