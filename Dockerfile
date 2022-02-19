# syntax=docker/dockerfile:1
FROM python:3.8

WORKDIR /usr/app

COPY ./requirements.txt /usr/app/requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /usr/app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1

COPY src/ usr/app/
