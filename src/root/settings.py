""" File contains global parameters of the project. """

from os import getenv


DEBUG = getenv('DEBUG', '1') in {'1', 'true', 'True'}
DATABASE_URL = getenv('DB_URL', 'postgres://postgres@postgres:5432/covid19')
SENTRY_URL = getenv('SN_URL')
BROKER_URL = getenv('MB_URL', 'amqp://guest:guest@rabbit:5672/')
CELERY_WORKERS = int(getenv('CELERY_WORKERS', '1'))

DATA_FILENAME = 'WHO-COVID-19-global-data.csv'
