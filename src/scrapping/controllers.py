from flask import request
from sqlalchemy import func

from scrapping.bp import bp
from scrapping.models import session_scope, Covid19
from scrapping.schemas import ARGUMENTS_SCHEMA, COVID19_SCHEMA


@bp.route('/<country>/<date>')
def country_by_date(country: str, date: str):
    country_upper = country.upper()
    arguments = ARGUMENTS_SCHEMA.load({'date': date})
    with session_scope() as session:
        record = session.query(Covid19).filter(
            Covid19.countries_iso_alpha_2 == country_upper,
            Covid19.record_date == arguments['date']
        ).one()
        result = COVID19_SCHEMA.dump(record)
    return result


@bp.route('/<country>')
def total_to_date_by_country(country: str):
    country_upper = country.upper()
    arguments = ARGUMENTS_SCHEMA.load(request.args)
    with session_scope() as session:
        record = session.query(
            func.max(Covid19.record_date).label('date'),
            func.sum(Covid19.new_cases).label('total_cases'),
            func.sum(Covid19.new_death).label('total_death')
        ).group_by(
            Covid19.countries_iso_alpha_2
        ).filter(
            Covid19.countries_iso_alpha_2 == country_upper,
            Covid19.record_date <= arguments['date']
        ).one()
        result = COVID19_SCHEMA.load({
            "date": record.date,
            "country": country_upper,
            "death": record.total_death,
            "cases": record.total_cases,
        })
    return COVID19_SCHEMA.dump(result)


@bp.route('/world')
def world_total_to_date():
    arguments = ARGUMENTS_SCHEMA.load(request.args)
    with session_scope() as session:
        record = session.query(
            func.max(Covid19.record_date).label('date'),
            func.sum(Covid19.new_cases).label('total_cases'),
            func.sum(Covid19.new_death).label('total_death')
        ).filter(Covid19.record_date <= arguments['date']).one()
        result = COVID19_SCHEMA.load({
            "date": record.date,
            "country": 'World',
            "death": record.total_death,
            "cases": record.total_cases,
        })
    return COVID19_SCHEMA.dump(result)


@bp.route('/world/<date>')
def daily_total(date: str):
    arguments = ARGUMENTS_SCHEMA.load({'date': date})
    with session_scope() as session:
        record = session.query(
            func.sum(Covid19.new_cases).label('new_cases'),
            func.sum(Covid19.new_death).label('new_death')
        ).filter(Covid19.record_date == arguments['date']).one()
        result = COVID19_SCHEMA.load({
            "date": arguments['date'],
            "country": 'World',
            "cases": record.new_cases,
            "death": record.new_death,
        })
    return COVID19_SCHEMA.dump(result)
