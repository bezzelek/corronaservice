import typing as t
from datetime import date
from unittest import TestCase

from flask.testing import FlaskClient

from root.db import BaseModel, engine, session_scope
from scrapping.models import Covid19
from app import app


class AppTests(TestCase):
    client: t.ClassVar[FlaskClient]

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()

        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        add_record = Covid19(
            record_date=date(2020, 5, 27),
            countries_iso_alpha_2='UA',
            country_name='Ukraine',
            new_death=10,
            new_cases=100
        )
        with session_scope() as session:
            session.add(add_record)

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.client.__exit__()

    def test_health_check(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200, msg='Health check is not ok!')

    def test_country_and_date_controller(self):
        response = self.client.get('/UA/2020-05-27')
        expect = {
            'cases': 100,
            'country': 'Ukraine',
            'date': '2020-05-27',
            'death': 10
        }
        self.assertEquals(response.status_code, 200, msg='Health check is not ok!')
        self.assertDictEqual(response.json, expect, msg='Check is not ok!')
