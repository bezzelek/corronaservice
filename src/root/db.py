import typing as t
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from root.settings import DATABASE_URL, DEBUG

BaseModel = declarative_base()
engine = create_engine(DATABASE_URL, echo=DEBUG)
SessionMaker = sessionmaker(bind=engine)


@contextmanager
def session_scope() -> t.Iterator[Session]:
    """ Provide a transactional scope around a series of operations. """
    session = SessionMaker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
