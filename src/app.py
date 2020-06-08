""" Main module which starts application. It contains Flask app declaration and healthcheck controller. """

import typing as t
from socket import gethostname

from flask import Flask, jsonify

from scrapping.bp import bp as scrapping_bp


app = Flask('Coronavirus data')
app.register_blueprint(scrapping_bp, url_prefix='/')


@app.route('/')
def index() -> t.Dict[str, t.Union[str, bool]]:
    """ Healthcheck end point.

     :return: Information about service and it's parameters.
    """
    return jsonify({'service': app.name, 'debug': app.debug, 'host': gethostname()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # nosec
