FROM python:3.10.10-slim as pip-installed

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/

RUN apt-get update && apt-get install -y nano wget

WORKDIR app

COPY requirements.txt .
COPY scripts/* .
COPY alembic.ini .
COPY ./environment/dev/dev.env ./.env

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM pip-installed

COPY app ./app
COPY tests ./tests