import logging

from dependency_injector.wiring import inject, Provide
from flask import json, request

from pydas_metadata.contexts import BaseContext

from pydas.signals import SignalFactory
from pydas.constants import FeatureToggles
from pydas.containers import ApplicationContainer


@inject
def handle_base_server_error(error,
                             metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    logging.info("Handling base server error")
    should_handle_events = metadata_context.get_feature_toggle(
        FeatureToggles.event_handlers)
    if should_handle_events is True:
        # Send the on_error signal
        logging.debug("Signalling on-error event handlers")
        SignalFactory.on_error.send(
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
