import typing as t
from datetime import date

from flask.testing import FlaskClient
from flask import Response

from helpers.testing import DBTestCase
from root.db import session_scope
from scrapping.models import Covid19
from app import app


class AppTests(DBTestCase):
    client: t.ClassVar[FlaskClient]

    @classmethod
    def setUpClass(cls) -> None:
        @app.route('/e')
        def unexpected_error():
            raise Exception
        super().setUpClass()

    def test_health_check(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200, msg='Health check is not ok!')

    def test_unexpected_error(self):
        response: Response = self.client.get('/e')
        self.assertEquals(response.status_code, 500, msg='Unexpected server error processed.')
        self.assertEquals(response.content_type, 'application/json')


class CountryByDateTests(DBTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with session_scope() as session:
            session.add(
                Covid19(
                    record_date=date(2020, 5, 27),
                    countries_iso_alpha_2='UA',
                    country_name='Ukraine',
                    new_death=10,
                    new_cases=100
                )
            )

    def test_country_by_date_controller(self):
        expect = {
            'cases': 100,
            'country': 'Ukraine',
            'date': '2020-05-27',
            'death': 10
        }

        response = self.client.get('/UA/2020-05-27')
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

        response = self.client.get('/ua/2020-05-27')
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

    def test_no_result_found(self):
        response = self.client.get('/UA/2020-05-28')
        self.assertEquals(response.status_code, 404, msg='Unexpected data exists.')

    def test_no_country_found(self):
        response = self.client.get('/US/2020-05-27')
        self.assertEquals(response.status_code, 404, msg='Unexpected data exists.')

    def test_bad_date_format(self):
        response = self.client.get('/UA/20200527')
        self.assertEquals(response.status_code, 400, msg='Wrong date. Success validation.')


class CountryTotalTests(DBTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with session_scope() as session:
            session.add_all([
                Covid19(
                    record_date=date(2020, 5, 27),
                    countries_iso_alpha_2='UA',
                    country_name='Ukraine',
                    new_death=10,
                    new_cases=100
                ),
                Covid19(
                    record_date=date(2020, 5, 28),
                    countries_iso_alpha_2='UA',
                    country_name='Ukraine',
                    new_death=5,
                    new_cases=50
                )
            ])

    def test_total_to_date_by_country_controller(self):
        response = self.client.get('/UA?date=2020-05-27')
        expect = {
            'cases': 100,
            'country': 'Ukraine',
            'date': '2020-05-27',
            'death': 10
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

        response = self.client.get('/ua?date=2020-05-28')
        expect = {
            'cases': 150,
            'country': 'Ukraine',
            'date': '2020-05-28',
            'death': 15
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

    def test_for_future_date(self):
        response = self.client.get('/UA?date=2020-05-29')
        expect = {
            'cases': 150,
            'country': 'Ukraine',
            'date': '2020-05-28',
            'death': 15
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

    def test_for_past_date(self):
        response = self.client.get('/UA?date=2020-05-26')
        self.assertEquals(response.status_code, 404, msg='Unexpected data exists.')

    def test_no_country_found(self):
        response = self.client.get('/US')
        self.assertEquals(response.status_code, 404, msg='Unexpected data exists.')

    def test_bad_date_format(self):
        response = self.client.get('/UA?date=20200527')
        self.assertEquals(response.status_code, 400, msg='Wrong date. Success validation.')


class WorldTotalTests(DBTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with session_scope() as session:
            session.add_all([
                Covid19(
                    record_date=date(2020, 5, 27),
                    countries_iso_alpha_2='UA',
                    country_name='Ukraine',
                    new_death=10,
                    new_cases=100
                ),
                Covid19(
                    record_date=date(2020, 5, 28),
                    countries_iso_alpha_2='US',
                    country_name='United States of America',
                    new_death=20,
                    new_cases=200
                )
            ])

    def test_world_total_to_date_controller(self):
        response = self.client.get('/world?date=2020-05-27')
        expect = {
            'cases': 100,
            'country': 'World',
            'date': '2020-05-27',
            'death': 10
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

        response = self.client.get('/world?date=2020-05-28')
        expect = {
            'cases': 300,
            'country': 'World',
            'date': '2020-05-28',
            'death': 30
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

    def test_for_future_date(self):
        response = self.client.get('/world?date=2020-05-29')
        expect = {
            'cases': 300,
            'country': 'World',
            'date': '2020-05-28',
            'death': 30
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

    def test_for_past_date(self):
        response = self.client.get('/world?date=2020-05-26')
        self.assertEquals(response.status_code, 404, msg='Unexpected data exists.')

    def test_bad_date_format(self):
        response = self.client.get('/world?date=20200527')
        self.assertEquals(response.status_code, 400, msg='Wrong date. Success validation.')


class WorldTotalByDateTests(DBTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with session_scope() as session:
            session.add_all([
                Covid19(
                    record_date=date(2020, 5, 27),
                    countries_iso_alpha_2='UA',
                    country_name='Ukraine',
                    new_death=10,
                    new_cases=100
                ),
                Covid19(
                    record_date=date(2020, 5, 27),
                    countries_iso_alpha_2='US',
                    country_name='United States of America',
                    new_death=20,
                    new_cases=200
                )
            ])

    def test_world_total_by_date_controller(self):
        response = self.client.get('/world/2020-05-27')
        expect = {
            'cases': 300,
            'country': 'World',
            'date': '2020-05-27',
            'death': 30
        }
        self.assertEquals(response.status_code, 200, msg='Unexpected status code.')
        self.assertDictEqual(response.json, expect, msg='Unexpected data.')

    def test_bad_date_format(self):
        response = self.client.get('/world/20200527')
        self.assertEquals(response.status_code, 400, msg='Wrong date. Success validation.')

    def test_no_result_found(self):
        response = self.client.get('/world/2020-05-29')
        self.assertEquals(response.status_code, 404, msg='Unexpected data exists.')
