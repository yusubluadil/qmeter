FROM python:3.9-slim

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput
