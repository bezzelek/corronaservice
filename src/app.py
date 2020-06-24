""" Main module which starts application. It contains Flask app declaration and healthcheck controller. """

from root.app import app
from scrapping.bp import bp as scrapping_bp


app.register_blueprint(scrapping_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
