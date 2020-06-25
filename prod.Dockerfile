ARG image

FROM ${image} as ci

ENV FLASK_ENV="production" \
    DEBUG="false"

COPY . /app/
CMD ["gunicorn", "--config", "python:root.gunicorn", "app:app"]
