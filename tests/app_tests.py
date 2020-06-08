import typing as t
from datetime import datetime, date

from unittest import TestCase

from flask.testing import FlaskClient

from app import app
from scrapping.models import BaseModel, engine, Covid19, session_scope


class AppTests(TestCase):
    client: t.ClassVar[FlaskClient]

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()

        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        test_date = datetime.strptime('2020-05-27', "%Y-%m-%d").date()
        add_record = Covid19(
            record_date=date(2020, 05, 27),
            countries_iso_alpha_2='UA',
            country_name='Ukraine',
            new_death=10,
            new_cases=100)
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
        expect = {'cases': 100,
                  'country': 'Ukraine',
                  'date': '2020-05-27',
                  'death': 10}
        self.assertEquals(response.status_code, 200, msg='Health check is not ok!')
        self.assertDictEqual(response.json, dict(expect), msg='Check is not ok!')
