from datetime import datetime
from socket import gethostname

from flask import Flask, jsonify, request
from sqlalchemy import and_, func, literal

from scrapping.models import Covid19, session_scope
from scrapping.schemas import Covid19CountrySchema, Covid19TotalSchema, ArgumentsSchema

app = Flask('Coronavirus data')


@app.route('/')
def index():
    return jsonify({'service': app.name, 'debug': app.debug, 'host': gethostname()})


@app.route('/<country>/<date>')
def country_by_date(country: str, date: str):
    country_upper = country.upper()
    date_style = datetime.strptime(date, "%Y-%m-%d").date()
    with session_scope() as session:
        record = session.query(Covid19).filter_by(countries_iso_alpha_2=country_upper, record_date=date_style).one()
    schema = Covid19CountrySchema()
    result = schema.dump(record)

    return result


@app.route('/<country>')
def total_to_date_by_country(country: str):
    country_upper = country.upper()
    argument_schema = ArgumentsSchema()
    arguments = argument_schema.load(request.args)
    with session_scope() as session:
        record = session.query(
            func.sum(Covid19.new_cases).label('total_cases'),
            func.sum(Covid19.new_death).label('total_death')
        ).group_by(
            Covid19.countries_iso_alpha_2
        ).filter(
            and_(
                Covid19.countries_iso_alpha_2 == country_upper,
                Covid19.record_date <= arguments['date']
            )
        ).one()
    schema = Covid19TotalSchema()
    result = schema.dump({
        "record_date": arguments['date'],
        "country_name": country_upper,
        "total_death": record.total_death,
        "total_cases": record.total_cases,
    })
    return result


@app.route('/total')
def world_total_to_date():
    argument_schema = ArgumentsSchema()
    arguments = argument_schema.load(request.args)
    with session_scope() as session:
        record = session.query(
            func.sum(Covid19.new_cases).label('total_cases'),
            func.sum(Covid19.new_death).label('total_death')
        ).filter(Covid19.record_date <= arguments['date']).one()
    schema = Covid19TotalSchema()
    result = schema.dump({
        "record_date": arguments['date'],
        "country_name": 'World',
        "total_death": record.total_death,
        "total_cases": record.total_cases,
    })
    return result


@app.route('/daily_total/<date>')
def daily_total(date: str):
    argument_schema = ArgumentsSchema()
    arguments = argument_schema.load({'date': date})
    with session_scope() as session:
        record = session.query(
            literal('World').label('country'),
            func.max(Covid19.record_date).label('date'),
            func.sum(Covid19.new_cases).label('new_cases'),
            func.sum(Covid19.new_death).label('new_death')
        ).filter(Covid19.record_date == arguments['date']).one()
    schema = Covid19CountrySchema()
    result = schema.load(record._asdict())
    return schema.dump(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
