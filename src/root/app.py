""" Main module which starts application. It contains Flask app declaration and healthcheck controller. """

import typing as t
from socket import gethostname

from flask import Flask
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from root.settings import DEBUG


app = Flask('Covid-19 Data Service')
app.config.update({
    'DEBUG': DEBUG,
    'JSON_SORT_KEYS': False
})


class ErrorSchema(Schema):
    """ Unified schema of server errors. """
    message = fields.Str()
    details = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()), required=False)


class StatusSchema(Schema):
    """ Unified schema of healthcheck endpoint. """
    service = fields.Str()
    debug = fields.Bool()
    host = fields.Str()


@app.route('/')
def index():
    """ Healthcheck end point.

    :return: Information about service and it's parameters.
    """
    return StatusSchema().load({
        'service': app.name,
        'debug': app.debug,
        'host': gethostname()
    })


@app.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    """ Handler for marshmallow validation error. """
    return ErrorSchema().load({
        'message': 'Bad Request',
        'details': error.messages
    }), 400


@app.errorhandler(404)
@app.errorhandler(NoResultFound)
@app.errorhandler(MultipleResultsFound)
def handle_db_error(_error: t.Union[NoResultFound, MultipleResultsFound]):
    """ Handler for db errors and unexpected paths. """
    return ErrorSchema().load({
        'message': 'Not Found',
    }), 404


@app.errorhandler(500)
def handle_unexpected_error(_error: Exception):
    """ Handler for unexpected errors. """
    return ErrorSchema().load({
        'message': 'Internal Server Error',
    }), 500
