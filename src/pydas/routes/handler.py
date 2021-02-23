from flask import Blueprint, current_app
from flask.json import jsonify

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Handler

from pydas import constants, scopes
from pydas.containers import metadata_container
from pydas.routes.utils import verify_scopes

handler_bp = Blueprint('handlers',
                       'pydas.routes.handler',
                       url_prefix='/api/v1/handlers')


@handler_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.HANDLERS_READ})
def handlers_index():
    """Retrieves all handlers from data store and returns a JSON array response object."""
    metadata_context: BaseContext = metadata_container.context_factory(
        current_app.config['DB_DIALECT'], **current_app.config['DB_CONFIG'])
    session_maker = metadata_context.get_session_maker()
    session = session_maker()
    query = session.query(Handler)
    handlers = query.all()

    return jsonify([json(handler) for handler in handlers])
