from datetime import date as dd

from marshmallow import Schema, fields


class LenientDate(fields.Date):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dd):
            return value
        return super()._deserialize(value, attr, data, **kwargs)


class Covid19CountrySchema(Schema):
    date = LenientDate(required=True, attribute='record_date')
    country = fields.Str(required=True, attribute='country_name')
    new_death = fields.Int(required=True)
    new_cases = fields.Int(required=True)


class Covid19TotalSchema(Schema):
    date = LenientDate(required=True, attribute='record_date')
    country = fields.Str(required=True, attribute='country_name')
    total_death = fields.Int(required=True)
    total_cases = fields.Int(required=True)


class ArgumentsSchema(Schema):
    date = fields.Date(missing=dd.today)
