""" Controllers that returns requested data. """

import typing as t
from datetime import date as dd

from flask_apispec import use_kwargs, marshal_with, doc
from marshmallow import fields
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from root.db import session
from root.app import ERROR_SCHEMA

from scrapping.bp import bp
from scrapping.models import Covid19
from scrapping.schemas import ARGUMENTS_SCHEMA, COVID19_SCHEMA


@bp.route('/<country>/<date>')
@doc(params={
    'date': {'type': 'date', 'description': 'Date in format `YYYY-mm-DD`'},
    'country': {'description': 'Country name in ISO Alpha-2 format. Example: "UA" - Ukraine'}
})
@marshal_with(COVID19_SCHEMA, code=200, description='Returns data for the requested date in requested country')
@marshal_with(ERROR_SCHEMA, code=422, description='Validation error')
@marshal_with(ERROR_SCHEMA, code=404, description='No data found for requested value')
def country_by_date(country: str, date: str) -> t.Dict[str, t.Union[dd, str, int]]:
    """ Controller that returns data for the requested date in requested country.

    :param country: Name of the country which expressed in ISO Alpha-2 format. Example: "UA" - Ukraine
    :param date: Date which expressed in format 2020-01-30
    :return: Number of cases and death registered in specific country in specific day.
    """
    country_upper = country.upper()
    arguments = ARGUMENTS_SCHEMA.load({'date': date})
    record = session.query(Covid19).filter(
        Covid19.countries_iso_alpha_2 == country_upper,
        Covid19.record_date == arguments['date']
    ).one()
    return record


@bp.route('/<country>')
@doc(params={
    'country': {'description': 'Country name in ISO Alpha-2 format. Example: "UA" - Ukraine'}
})
@use_kwargs({'date': fields.Date()}, locations=['query'])
@marshal_with(COVID19_SCHEMA, code=200, description='Returns calculated data for the requested country')
@marshal_with(ERROR_SCHEMA, code=422, description='Validation error')
@marshal_with(ERROR_SCHEMA, code=404, description='No data found for requested value')
def total_to_date_by_country(country: str, date: dd = None) -> t.Dict[str, t.Union[dd, str, int]]:
    """ Controller that returns calculated data about amount of cases and death from the beginning of statistical
    calculations for the requested country.

    :param country: Name of the country which expressed in ISO Alpha-2 format. Example: "UA" - Ukraine
    :return: Number of cases and death registered in country from the beginning of statistical calculations
    """
    date = date or dd.today()
    country_upper = country.upper()
    record = session.query(
        func.max(Covid19.record_date).label('date'),
        func.sum(Covid19.new_cases).label('total_cases'),
        func.sum(Covid19.new_death).label('total_death'),
        Covid19.country_name
    ).group_by(
        Covid19.country_name
    ).filter(
        Covid19.countries_iso_alpha_2 == country_upper,
        Covid19.record_date <= date
    ).one()
    result = {
        "record_date": record.date,
        "country_name": record.country_name,
        "new_death": record.total_death,
        "new_cases": record.total_cases,
    }
    return result


@bp.route('/world')
@use_kwargs({'date': fields.Date()}, locations=['query'])
@marshal_with(COVID19_SCHEMA, code=200, description='Returns calculated data fro the whole World')
@marshal_with(ERROR_SCHEMA, code=422, description='Validation error')
@marshal_with(ERROR_SCHEMA, code=404, description='No data found for requested value')
def world_total_to_date(date: dd = None) -> t.Dict[str, t.Union[dd, str, int]]:
    """ Controller that returns calculated data about amount of cases and death from the beginning of statistical
    calculations in whole World

    :return: Calculated data about amount of cases and death from the beginning of statistical calculations in whole
    World.
    """
    date = date or dd.today()
    record = session.query(
        func.max(Covid19.record_date).label('date'),
        func.sum(Covid19.new_cases).label('total_cases'),
        func.sum(Covid19.new_death).label('total_death')
    ).filter(Covid19.record_date <= date).one()
    if record.date is None:
        raise NoResultFound
    result = {
        "record_date": record.date,
        "country_name": 'World',
        "new_death": record.total_death,
        "new_cases": record.total_cases,
    }
    return result


@bp.route('/world/<date>')
@doc(params={
    'date': {'type': 'date', 'description': 'Date in format `YYYY-mm-DD`'}
})
@marshal_with(COVID19_SCHEMA, code=200, description='Returns calculated data fro the whole World for specific day')
@marshal_with(ERROR_SCHEMA, code=422, description='Validation error')
@marshal_with(ERROR_SCHEMA, code=404, description='No data found for requested value')
def world_total_by_date(date: str) -> t.Dict[str, t.Union[dd, str, int]]:
    """ Controller that returns calculated data about amount of cases and death in whole World during specific day.

    :param date: Date which expressed in format 2020-01-30
    :return: Calculated data about amount of cases and death in whole World during specific day.
    """
    arguments = ARGUMENTS_SCHEMA.load({'date': date})
    record = session.query(
        func.sum(Covid19.new_cases).label('new_cases'),
        func.sum(Covid19.new_death).label('new_death')
    ).filter(Covid19.record_date == arguments['date']).one()
    if record.new_cases is None:
        raise NoResultFound
    result = {
        "record_date": arguments['date'],
        "country_name": 'World',
        "new_cases": record.new_cases,
        "new_death": record.new_death,
    }
    return result
