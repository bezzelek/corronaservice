""" Module contains schemas to represent data on our views. """

from datetime import date as dd

from marshmallow import Schema, fields


class LenientDate(fields.Date):
    """ More lenient version of the date field that allow to load date objects. """
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dd):
            return value
        return super()._deserialize(value, attr, data, **kwargs)


class Covid19Schema(Schema):
    """ Main schema for our data. """
    country = fields.Str(required=True, attribute='country_name')
    date = LenientDate(required=True, attribute='record_date')
    cases = fields.Int(required=True, attribute='new_cases')
    death = fields.Int(required=True, attribute='new_death')


class ArgumentsSchema(Schema):
    """ Schema for parsing of request arguments. """
    date = fields.Date(missing=dd.today)


COVID19_SCHEMA = Covid19Schema()
ARGUMENTS_SCHEMA = ArgumentsSchema()
