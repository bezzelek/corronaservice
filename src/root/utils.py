import typing as t
from unittest.case import TestCase

from flask.testing import FlaskClient

from root.app import app
from root.db import db


class DBTestCase(TestCase):
    client: t.ClassVar[FlaskClient]

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        db.drop_all()
        db.create_all()
