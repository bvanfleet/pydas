'''
The python Data Acquisition Service (pyDAS) package contains the modules
necessary for performing data acquisition and dataset generation.
'''
from flask import Flask, url_for, redirect
from flask_cors import CORS

from sqlalchemy.exc import OperationalError

from pydas import routes, signals
from pydas.containers import ApplicationContainer
from pydas.handlers import handle_base_server_error
from pydas.handlers import handle_database_error
from pydas.routes import (acquire,
                          archives,
                          company,
                          configuration,
                          feature,
                          handler,
                          option,
                          statistics)
from pydas.routes.swagger import SWAGGER_URL

# pylint: disable=no-member,unused-variable
# Ignoring warnings for the app-registered functions and app logging.


def create_app(config_filename: str = 'pydas.yaml'):
    """The pyDAS application factory for configuring the server object at runtime."""
    app = Flask(__name__)

    app_container = ApplicationContainer(app=app)
    app_container.config.from_yaml(config_filename)
    app.config["TESTING"] = app_container.config.testing()
    app_container.init_resources()
    app.container = app_container

    app.logger.info("Starting pyDAS API app")
    CORS(app)

    # Route registrations
    app.register_blueprint(routes.feature_bp)
    app.register_blueprint(routes.company_bp)
    app.register_blueprint(routes.handler_bp)
    app.register_blueprint(routes.statistics_bp)
    app.register_blueprint(routes.configuration_bp)
    app.register_blueprint(routes.option_bp)
    app.register_blueprint(routes.acquire_bp)
    app.register_blueprint(routes.archives_bp)
    app.register_blueprint(routes.swaggerui_bp, url_prefix=SWAGGER_URL)

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

    try:
        app.container.wire(
            modules=[acquire,
                     archives,
                     signals,
                     company,
                     configuration,
                     feature,
                     handler,
                     option,
                     statistics])
    except Exception as exc:
        app.logger.error("Unable to wire dependency injection!", exc_info=exc)
        exit(1)

    try:
        with app.app_context():
            signals.SignalFactory.register_signals()
    except RuntimeError as exc:
        app.logger.warning(
            'Unable to register signals, please check that blinker is installed: %s',
            exc)

    return app


__version__ = "1.1.0"
