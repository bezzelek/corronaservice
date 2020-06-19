import typing as t
from unittest.case import TestCase

from flask.testing import FlaskClient

from app import app
from root.db import BaseModel, engine


class DBTestCase(TestCase):
    client: t.ClassVar[FlaskClient]

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
