""" Main module which starts application. It contains Flask app declaration and healthcheck controller. """

import typing as t
from socket import gethostname

from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from root.settings import DEBUG
from scrapping.bp import bp as scrapping_bp
from scrapping.schemas import ERROR_SCHEMA

app = Flask('Coronavirus data')
app.register_blueprint(scrapping_bp, url_prefix='/')


@app.route('/')
def index() -> t.Dict[str, t.Union[str, bool]]:
    """ Healthcheck end point.

     :return: Information about service and it's parameters.
    """
    return jsonify({'service': app.name, 'debug': app.debug, 'host': gethostname()})


@app.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    resp = ERROR_SCHEMA.load({
        'code': 400,
        'message': 'Error during validation of input data.',
        'details': error.messages
    })
    return jsonify(resp), 400


@app.errorhandler(NoResultFound)
@app.errorhandler(MultipleResultsFound)
def handle_db_error(_error: t.Union[NoResultFound, MultipleResultsFound]):
    resp = ERROR_SCHEMA.load({
        'code': 404,
        'message': 'No result for requested values.',
    })
    return jsonify(resp), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
