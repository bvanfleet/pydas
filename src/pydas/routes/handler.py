from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, request
from flask.json import jsonify

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Handler

from pydas import constants
from pydas.containers import ApplicationContainer

handler_bp = Blueprint('handlers',
                       'pydas.routes.handler',
                       url_prefix='/api/v1/handlers')


@handler_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.HANDLERS_READ},
               current_app,
               request)
@inject
def handlers_index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    """Retrieves all handlers from data store and returns a JSON array response object."""
    session = metadata_context.get_session()
    query = session.query(Handler)
    handlers = query.all()

    return jsonify([json(handler) for handler in handlers])
