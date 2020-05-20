import typing as t
from contextlib import contextmanager
from datetime import datetime, date

from sqlalchemy import create_engine, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from root.settings import DATABASE_URL

BaseModel = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
SESSION = Session()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Covid19(BaseModel):
    __tablename__ = 'covid19'
    __table_args__ = (
        UniqueConstraint('record_date', 'countries_iso_alpha_2'),
    )

    id = Column(Integer, primary_key=True)
    record_date = Column(Date)
    countries_iso_alpha_2 = Column(String(length=2))
    country_name = Column(String)
    region_by_who = Column(String)
    new_death = Column(Integer)
    total_death = Column(Integer)
    new_cases = Column(Integer)
    total_cases = Column(Integer)

    @staticmethod
    def column_cast(column: str) -> t.Union[date, int, str]:
        """ Функция для преобразования данных.

        :param column: принимает аргумент колонку, тип аргумента - строка
        column - переменная
        t.Union[None, int, float] - возвращаемый тип данных

        :return: преобразованій тип данных
        """
        if len(column) == 10 and column.count("-") == 2:
            return datetime.strptime(column, "%Y-%m-%d").date()  # strptime - переганяет строку во время,
                                                                 # strftime - наоборот
        if column.isdecimal():  # isdecimal - проверка на целое число
            return int(column)

        return column  # ничего не делаем

    @classmethod
    def from_row(cls, *columns):
        column_headers = (
            'record_date', 'countries_iso_alpha_2',
            'country_name', 'region_by_who',
            'new_death', 'total_death',
            'new_cases', 'total_cases',
        )
        # casted_columns = []
        # for num in row:
        #     casted_columns.append(column_cast(num))
        casted_columns = [cls.column_cast(column) for column in columns]
        row_data = dict(zip(column_headers, casted_columns))
        return cls(**row_data)


if __name__ == '__main__':
    BaseModel.metadata.create_all(engine)
