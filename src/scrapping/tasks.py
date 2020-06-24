""" Module that contains our main task that downloads and updates data in our database. """

import typing as t
import csv
from datetime import datetime, timedelta
from logging import getLogger, basicConfig, INFO

from celery.task import periodic_task
from marshmallow import ValidationError
from sqlalchemy import func

from root.settings import DATA_FILENAME
from root.db import transaction
from scrapping.models import Covid19
from scrapping.schemas import COVID19_LOAD_SCHEMA
from scrapping.scrapper import download_csv


logger = getLogger()


@periodic_task(run_every=timedelta(hours=1))
def store_csv_data() -> None:
    """ Function launches downloading of the file with data from the source. When we have some data in our base,
    function will update data for the last two days or if data not exist function will load all the data from the
    source.
    """
    logger.info('Downloading data file...')
    csv_path = download_csv(DATA_FILENAME)
    with transaction() as session, open(csv_path) as covidcsv:
        logger.info('Parsing data file...')
        reader = csv.reader(covidcsv)
        next(reader)  # skip table headers
        covid19_buffer: t.List[Covid19] = []

        data_exists = bool(session.query(Covid19).count())
        if data_exists:
            logger.info('Cleaning data for the last two days...')
            yesterday = (datetime.now() - timedelta(days=1)).date()
            session.query(Covid19).filter(Covid19.record_date >= yesterday).delete()

        max_date = session.query(func.max(Covid19.record_date).label('date')).one()

        for index, row in enumerate(reader):  # type: t.Tuple[int, t.List[str]]
            try:
                record = COVID19_LOAD_SCHEMA.load({
                    'record_date': row[0],
                    'countries_iso_alpha_2': row[1],
                    'country_name': row[2],
                    'new_cases': row[4],
                    'new_death': row[6],
                })
            except ValidationError as err:
                logger.warning('Error during loading of {} line: {}', index + 1, err.messages)
                continue
            if data_exists and record.record_date <= max_date.date:
                continue
            covid19_buffer.append(record)
        logger.info('Commit of {} records...', len(covid19_buffer))
        session.add_all(covid19_buffer)


if __name__ == '__main__':
    basicConfig(level=INFO)
    store_csv_data()
