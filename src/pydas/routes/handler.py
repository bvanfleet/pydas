from flask import Blueprint
from flask.json import jsonify

from pydas_metadata import json
from pydas_metadata.models import Handler

from pydas import constants
from pydas import scopes
from pydas.routes.utils import get_session, verify_scopes

handler_bp = Blueprint('handlers',
                       'pydas.routes.handler',
                       url_prefix='/api/v1/handlers')


@handler_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.HANDLERS_READ})
def handlers_index():
    """Retrieves all handlers from data store and returns a JSON array response object."""
    session = get_session()
    query = session.query(Handler)
    handlers = query.all()

    return jsonify([json(handler) for handler in handlers])
