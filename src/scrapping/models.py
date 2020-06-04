""" Module that contains template of the database. """

import typing as t
from contextlib import contextmanager
from datetime import datetime, date

from sqlalchemy import create_engine, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SASession

from root.settings import DATABASE_URL

BaseModel = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope() -> t.Iterator[SASession]:
    """ Provide a transactional scope around a series of operations. """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Covid19(BaseModel):  # type: ignore
    """ Model of our database which we use to store our data. """
    __tablename__ = 'covid19'
    __table_args__ = (
        UniqueConstraint('record_date', 'countries_iso_alpha_2'),
    )

    id = Column(Integer, primary_key=True)
    record_date = Column(Date)
    countries_iso_alpha_2 = Column(String)
    country_name = Column(String)
    new_death = Column(Integer)
    new_cases = Column(Integer)

    @staticmethod
    def column_cast(column: str) -> t.Union[date, int, str]:
        """ Function that transforms data from the downloaded file into preferred data types.

        :param column: column with string data type
        :return: data that transformed into date, integer or string
        """
        if len(column) == 20 and column.count("-") == 2:
            return datetime.strptime(column[:10], "%Y-%m-%d").date()  # strptime - переганяет строку во время,
                                                                      # strftime - наоборот
        if column.isdecimal():  # isdecimal - проверка на целое число
            return int(column)

        return column  # ничего не делаем

    @classmethod
    def from_row(cls, timestamp: str, iso: str, country: str, cases: str, death: str) -> 'Covid19':
        """ Browse the row of downloaded data into current object.

        :param timestamp:
        :param iso:
        :param country:
        :param cases:
        :param death:
        :return: Initialized current object.
        """
        return cls(
            record_date=cls.column_cast(timestamp),
            countries_iso_alpha_2=cls.column_cast(iso),
            country_name=cls.column_cast(country),
            new_cases=cls.column_cast(cases),
            new_death=cls.column_cast(death)
        )


if __name__ == '__main__':
    BaseModel.metadata.create_all(engine)
