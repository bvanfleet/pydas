import logging
from flask import current_app, json, request
from pydas_metadata.models import FeatureToggle
from pydas.routes.utils import get_session
from pydas.signals import SignalFactory
from pydas.constants import FeatureToggles


def handle_base_server_error(error):
    logging.info("Handling base server error")
    session = get_session()
    feature_toggle = session.query(FeatureToggle).filter(
        FeatureToggle.name == FeatureToggles.event_handlers).one_or_none()
    if feature_toggle.is_enabled is True:
        # Send the on_error signal
        logging.debug("Signalling on-error event handlers")
        SignalFactory.on_error.send(
            current_app._get_current_object(),
            uri=request.endpoint,
            type='ERROR',
            exception=error.original_exception)

    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": "sDAS Server Failure",
        "description": "Unable to complete call to sDAS. Please contact the system administrator."
    })
    response.content_type = "application/json"
    return response


def handle_database_error(error):
    logging.info("Handling database connection error")
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": "sDAS Server Failure",
        "description": "Unable to connect to database. Please contact your system administrator to verify the username and the password."
    })
    response.content_type = "application/json"
    return response
