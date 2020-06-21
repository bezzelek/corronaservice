FROM python:3.8.3-alpine3.12
COPY ["requirements.txt", "requirements.dev.txt", "/app/"]

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
    && apk add --update --no-cache make bash libpq chromium chromium-chromedriver

RUN apk add --no-cache --virtual build \
    build-base \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    && pip install --no-cache-dir -r /app/requirements.dev.txt \
    && apk del build

ENV PYTHONPATH "$PYTHONPATH:/app/src"
WORKDIR /app
