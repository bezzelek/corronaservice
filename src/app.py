""" Main module which starts application. It contains Flask app declaration and healthcheck controller. """
import sentry_sdk
from flask_apispec import FlaskApiSpec
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from root.settings import SENTRY_URL
from root.app import app
from scrapping.bp import bp as scrapping_bp


app.register_blueprint(scrapping_bp, url_prefix='/')

app.config['APISPEC_SWAGGER_UI_URL'] = '/docs/'
docs = FlaskApiSpec(app)

if SENTRY_URL is not None:
    sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()]
    )

docs.register_existing_resources()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
