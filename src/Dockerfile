FROM python:3.12-slim-bookworm

ARG DOCKER_USER
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code

RUN apt-get update \
    && apt-get -y install libpq-dev gcc libgraphviz-dev \
    && pip install psycopg2

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

RUN mkdir /nltk_data
RUN chown $DOCKER_USER /nltk_data

RUN mkdir /code
WORKDIR /code

COPY . /code/

RUN mkdir /code/staticfiles
RUN DJANGO_SETTINGS_MODULE=config.settings python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "config.wsgi"]
