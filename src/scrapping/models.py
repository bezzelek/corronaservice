""" Module that contains template of the database. """

from sqlalchemy import Column, Integer, String, Date, UniqueConstraint

from root.db import BaseModel, db


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


if __name__ == '__main__':
    db.create_all()
