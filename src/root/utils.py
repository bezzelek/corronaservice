""" Project utils. """

import typing as t
from unittest.case import TestCase

from flask.testing import FlaskClient
from marshmallow import Schema

from root.app import app
from root.db import db


class DBTestCase(TestCase):
    """ Tests initialization. """
    client: t.ClassVar[FlaskClient]

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        db.drop_all()
        db.create_all()


class APISchema(Schema):
    """ Schema for dumping data. """
    def dump(self, obj: t.Any, *, many: bool = None):
        res = super().dump(obj, many=many)
        if not res:
            raise ValueError('Empty API response.')
        self.load(res, many=many)
        return res
