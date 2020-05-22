from datetime import date as dd

from marshmallow import Schema, fields


class LenientDate(fields.Date):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dd):
            return value
        return super()._deserialize(value, attr, data, **kwargs)


class Covid19Schema(Schema):
    country = fields.Str(required=True, attribute='country_name')
    date = LenientDate(required=True, attribute='record_date')
    cases = fields.Int(required=True, attribute='new_cases')
    death = fields.Int(required=True, attribute='new_death')


class ArgumentsSchema(Schema):
    date = fields.Date(missing=dd.today)


COVID19_SCHEMA = Covid19Schema()
ARGUMENTS_SCHEMA = ArgumentsSchema()
