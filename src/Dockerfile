FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

RUN mkdir /code
WORKDIR /code

COPY . /code/

RUN mkdir /code/staticfiles
RUN DJANGO_SETTINGS_MODULE=config.settings python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "config.wsgi"]
