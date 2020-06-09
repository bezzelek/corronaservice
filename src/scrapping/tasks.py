""" Module that contains our main task that downloads and updates data in our database. """

import typing as t
import csv
from datetime import datetime, timedelta

from celery.task import periodic_task
from sqlalchemy import func

from root.settings import DATA_FILENAME
from root.db import session_scope
from scrapping.models import Covid19
from scrapping.scrapper import download_csv


@periodic_task(run_every=timedelta(hours=1))
def store_csv_data() -> None:
    """ Function launches downloading of the file with data from the source. When we have some data in our base,
    function will update data for the last two days or if data not exist function will load all the data from the
    source.
    """
    csv_path = download_csv(DATA_FILENAME)
    with session_scope() as session, open(csv_path) as covidcsv:
        reader = csv.reader(covidcsv)
        next(reader)  # skip table headers
        covid19_buffer: t.List[Covid19] = []

        data_exists = bool(session.query(Covid19).count())
        if data_exists:
            yesterday = (datetime.now() - timedelta(days=1)).date()
            session.query(Covid19).filter(Covid19.record_date >= yesterday).delete()

        max_date = session.query(func.max(Covid19.record_date).label('date')).one()

        for row in reader:  # type: t.List[str]
            # row[0] - date
            # row[1] - country ISO code
            # row[2] - country name
            # row[4] - new cases
            # row[6] - new death
            record = Covid19.from_row(row[0], row[1], row[2], row[4], row[6])
            if data_exists and record.record_date <= max_date.date:
                continue
            covid19_buffer.append(record)

        session.add_all(covid19_buffer)


if __name__ == '__main__':
    store_csv_data()
