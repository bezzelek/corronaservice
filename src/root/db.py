import typing as t
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

from root.app import app
from root.settings import DATABASE_URL, DEBUG


app.config.update({
    'SQLALCHEMY_DATABASE_URI': DATABASE_URL,
    'SQLALCHEMY_ECHO': DEBUG,
})
db = SQLAlchemy(app)

BaseModel = db.Model
session = db.session


@contextmanager
def connection() -> t.Iterator[Session]:
    new_session = db.create_scoped_session()
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


@contextmanager
def transaction() -> t.Iterator[Session]:
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
