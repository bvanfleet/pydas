'''
The python Data Acquisition Service (pyDAS) package contains the modules
necessary for performing data acquisition and dataset generation.
'''
from flask import Flask, url_for, redirect
from flask_cors import CORS

from sqlalchemy.exc import OperationalError

from pydas.config import Config
from pydas.containers import config_container
from pydas.handlers import handle_base_server_error
from pydas.handlers import handle_database_error
from pydas.routes import (acquire_bp,
                          archives_bp,
                          company_bp,
                          configuration_bp,
                          feature_bp,
                          handler_bp,
                          option_bp,
                          statistics_bp,
                          swaggerui_bp)
from pydas.routes.swagger import SWAGGER_URL
from pydas.signals import SignalFactory

# pylint: disable=no-member,unused-variable
# Ignoring warnings for the app-registered functions and app logging.


def create_app(config_filename: str = 'pydas.yaml'):
    """The pyDAS application factory for configuring the server object at runtime."""
    config_container.config.from_yaml(config_filename)
    config_container.init_resources()

    app = Flask(__name__)
    app.logger.info("Starting sDAS API app")
    app.config.from_object(Config())
    CORS(app)

    try:
        with app.app_context():
            SignalFactory.register_signals()
    except RuntimeError as exc:
        app.logger.warning(
            'Unable to register signals, please check that blinker is installed: %s',
            exc)

    # Route registrations
    app.register_blueprint(feature_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(handler_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(configuration_bp)
    app.register_blueprint(option_bp)
    app.register_blueprint(acquire_bp)
    app.register_blueprint(archives_bp)
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    # Additional error handler registrations
    app.register_error_handler(OperationalError, handle_database_error)
    app.register_error_handler(500, handle_base_server_error)

    @app.route(f'{SWAGGER_URL}/dist/swagger')
    def dist():
        '''Returns a redirect for the Swagger UI config.yaml distribution.'''
        return redirect(url_for('static', filename="swagger-config.yaml"))

    @app.after_request
    def update_header(response):
        response.headers['server'] = f'pyDAS/{__version__}'
        return response

    return app


__version__ = "1.1.0"
