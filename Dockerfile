FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential wget unzip&& rm -rf /var/lib/apt/lists/*

RUN pip install uwsgi --no-cache-dir
ADD requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

WORKDIR /app

ADD . /app