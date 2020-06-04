""" File contains global parameters of the project. """

DATA_FILENAME = 'WHO-COVID-19-global-data.csv'
DATABASE_URL = 'postgres://postgres@127.0.0.1:5432/postgres'
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672/'
CELERY_WORKERS = 1
