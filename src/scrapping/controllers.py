""" Controllers that returns requested data. """

import typing as t
from datetime import date as dd

from flask import request
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from root.db import session
from scrapping.bp import bp
from scrapping.models import Covid19
from scrapping.schemas import ARGUMENTS_SCHEMA, COVID19_SCHEMA


@bp.route('/<country>/<date>')
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
    result = COVID19_SCHEMA.dump(record)
    return result


@bp.route('/<country>')
def total_to_date_by_country(country: str) -> t.Dict[str, t.Union[dd, str, int]]:
    """ Controller that returns calculated data about amount of cases and death from the beginning of statistical
    calculations for the requested country.

    :param country: Name of the country which expressed in ISO Alpha-2 format. Example: "UA" - Ukraine
    :return: Number of cases and death registered in country from the beginning of statistical calculations
    """
    country_upper = country.upper()
    arguments = ARGUMENTS_SCHEMA.load(request.args)
    record = session.query(
        func.max(Covid19.record_date).label('date'),
        func.sum(Covid19.new_cases).label('total_cases'),
        func.sum(Covid19.new_death).label('total_death'),
        Covid19.country_name
    ).group_by(
        Covid19.country_name
    ).filter(
        Covid19.countries_iso_alpha_2 == country_upper,
        Covid19.record_date <= arguments['date']
    ).one()
    result = COVID19_SCHEMA.load({
        "date": record.date,
        "country": record.country_name,
        "death": record.total_death,
        "cases": record.total_cases,
    })
    return COVID19_SCHEMA.dump(result)


@bp.route('/world')
def world_total_to_date() -> t.Dict[str, t.Union[dd, str, int]]:
    """ Controller that returns calculated data about amount of cases and death from the beginning of statistical
    calculations in whole World

    :return: Calculated data about amount of cases and death from the beginning of statistical calculations in whole
    World.
    """
    arguments = ARGUMENTS_SCHEMA.load(request.args)
    record = session.query(
        func.max(Covid19.record_date).label('date'),
        func.sum(Covid19.new_cases).label('total_cases'),
        func.sum(Covid19.new_death).label('total_death')
    ).filter(Covid19.record_date <= arguments['date']).one()
    if record.date is None:
        raise NoResultFound
    result = COVID19_SCHEMA.load({
        "date": record.date,
        "country": 'World',
        "death": record.total_death,
        "cases": record.total_cases,
    })
    return COVID19_SCHEMA.dump(result)


@bp.route('/world/<date>')
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
    result = COVID19_SCHEMA.load({
        "date": arguments['date'],
        "country": 'World',
        "cases": record.new_cases,
        "death": record.new_death,
    })
    return COVID19_SCHEMA.dump(result)
