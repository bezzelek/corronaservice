from socket import gethostname

from flask import Flask, jsonify, request
from sqlalchemy import func

from scrapping.models import Covid19, session_scope
from scrapping.schemas import COUNTRY_SCHEMA, TOTAL_SCHEMA, ARGUMENTS_SCHEMA


app = Flask('Coronavirus data')


@app.route('/')
def index():
    return jsonify({'service': app.name, 'debug': app.debug, 'host': gethostname()})


@app.route('/<country>/<date>')
def country_by_date(country: str, date: str):
    country_upper = country.upper()
    arguments = ARGUMENTS_SCHEMA.load({'date': date})
    with session_scope() as session:
        record = session.query(Covid19).filter(
            Covid19.countries_iso_alpha_2 == country_upper,
            Covid19.record_date == arguments['date']
        ).one()
        result = COUNTRY_SCHEMA.dump(record)
    return result


@app.route('/<country>')
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
        result = TOTAL_SCHEMA.load({
            "date": record.date,
            "country": country_upper,
            "total_death": record.total_death,
            "total_cases": record.total_cases,
        })
    return TOTAL_SCHEMA.dump(result)


@app.route('/world')
def world_total_to_date():
    arguments = ARGUMENTS_SCHEMA.load(request.args)
    with session_scope() as session:
        record = session.query(
            func.max(Covid19.record_date).label('date'),
            func.sum(Covid19.new_cases).label('total_cases'),
            func.sum(Covid19.new_death).label('total_death')
        ).filter(Covid19.record_date <= arguments['date']).one()
        result = TOTAL_SCHEMA.load({
            "date": record.date,
            "country": 'World',
            "total_death": record.total_death,
            "total_cases": record.total_cases,
        })
    return TOTAL_SCHEMA.dump(result)


@app.route('/world/<date>')
def daily_total(date: str):
    arguments = ARGUMENTS_SCHEMA.load({'date': date})
    with session_scope() as session:
        record = session.query(
            func.sum(Covid19.new_cases).label('new_cases'),
            func.sum(Covid19.new_death).label('new_death')
        ).filter(Covid19.record_date == arguments['date']).one()
        result = COUNTRY_SCHEMA.load({
            "date": arguments['date'],
            "country": 'World',
            "new_cases": record.new_cases,
            "new_death": record.new_death,
        })
    return COUNTRY_SCHEMA.dump(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
