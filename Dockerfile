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

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]


