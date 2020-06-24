""" Module contains schemas to represent data on our views. """

from datetime import date as dd

from marshmallow import Schema, fields, pre_load, post_load

from scrapping.models import Covid19


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


class Covid19LoadSchema(Schema):
    """ Schema for loading raw covid19 data. """
    __model__ = Covid19

    record_date = LenientDate()
    countries_iso_alpha_2 = fields.Str()
    country_name = fields.Str(required=False)
    new_death = fields.Int()
    new_cases = fields.Int()

    @staticmethod
    @pre_load
    def normalize_data(data, **_kwargs):
        """ Use ISO as Country when it empty, trim date timestamp to the date. """
        data['record_date'] = data['record_date'][:10]
        if data.get('country_name') is None:
            data['country_name'] = data['countries_iso_alpha_2']
        return data

    @post_load
    def to_model(self, data, **_kwargs):
        """ Serialization data into Alchemy model. """
        return self.__model__(**data)


COVID19_SCHEMA = Covid19Schema()
COVID19_LOAD_SCHEMA = Covid19LoadSchema()
ARGUMENTS_SCHEMA = ArgumentsSchema()
