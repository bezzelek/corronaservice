from datetime import date
from unittest import TestCase

from scrapping.models import Covid19


class Covid19Tests(TestCase):
    def test_column_cast_date(self):
        actual = Covid19.column_cast('2020-05-25  12:00:00')
        expected = date(2020, 5, 25)
        self.assertEquals(actual, expected, msg='Wrong date casting.')

    def test_column_cast_integer(self):
        actual = Covid19.column_cast('84654135')
        expected = 84654135
        self.assertEquals(actual, expected, msg='Wrong integer casting.')

    def test_column_cast_other(self):
        actual = Covid19.column_cast('Ukraine')
        expected = 'Ukraine'
        self.assertEquals(actual, expected, msg='Wrong string casting.')
