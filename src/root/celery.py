""" File contains settings of Celery. """
import sentry_sdk
from celery import Celery
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from root.settings import BROKER_URL, CELERY_WORKERS, SENTRY_URL

app = Celery('celery', broker=BROKER_URL)

app.conf.update({
    'task_default_delivery_mode': 'transient',
    'broker_connection_timeout': 5.0,
    'broker_connection_max_retries': 12,
    'worker_concurrency': CELERY_WORKERS,
    'worker_prefetch_multiplier': 1,
})

app.autodiscover_tasks(['scrapping'])


if SENTRY_URL is not None:
    sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[CeleryIntegration(), SqlalchemyIntegration()]
    )
