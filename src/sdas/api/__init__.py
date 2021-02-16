'''
sDAS REST sdas.api application for providing a method of access for both
metadata and data acquisition.
'''
from flask import Flask, url_for, redirect
from flask_cors import CORS

from sqlalchemy.exc import OperationalError

from sdas.api.config import ProductionConfig, setup_logging
from sdas.api.handlers import handle_base_server_error
from sdas.api.handlers import handle_database_error
from sdas.api.routes import (acquire_bp,
                             archives_bp,
                             company_bp,
                             configuration_bp,
                             feature_bp,
                             handler_bp,
                             option_bp,
                             statistics_bp,
                             swaggerui_bp)
from sdas.api.routes.swagger import SWAGGER_URL
from sdas.api.signals import SignalFactory

setup_logging()

app = Flask(__name__)
app.logger.info("Starting sDAS API app")  # pylint: disable=no-member
app.config.from_object(ProductionConfig())
CORS(app)

try:
    SignalFactory.register_signals()
except RuntimeError as exc:
    # pylint: disable=no-member
    app.logger.warning(
        'Unable to register signals, please check that blinker is installed')

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
