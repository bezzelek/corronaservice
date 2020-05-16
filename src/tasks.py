import csv
from datetime import datetime, timedelta

from celery import Celery
from sqlalchemy import literal

from models import session_scope, Covid19, SESSION
from scrapper import download_csv
from settings import DATA_FILENAME


# app = Celery()
#
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender):
#     sender.add_periodic_task(60.0, store_csv_data())   # 60 seconds
#
#
# @app.task
def store_csv_data():
    csv_path = download_csv(DATA_FILENAME)
    with session_scope() as session, open(csv_path) as covidcsv:
        reader = csv.reader(covidcsv)
        next(reader)  # skip table headers
        covid19_buffer = []

        data_exists = bool(session.query(Covid19).count())
        if data_exists:
            yesterday = (datetime.now() - timedelta(days=1)).date()
            session.query(Covid19).filter(Covid19.record_date >= yesterday).delete()

        for row in reader:
            record = Covid19.from_row(*row)
            if data_exists and record.record_date < yesterday:
                continue
            covid19_buffer.append(record)

        session.add_all(covid19_buffer)


if __name__ == '__main__':
    store_csv_data()
