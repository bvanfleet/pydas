from flask import Blueprint
from flask.json import jsonify

from metadata import json
from metadata.models import Handler

from sdas.api import constants
from sdas.api import scopes
from sdas.api.routes.utils import get_session, verify_scopes

handler_bp = Blueprint('handlers',
                       'sdas.api.routes.handler',
                       url_prefix='/api/v1/handlers')


@handler_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.HANDLERS_READ})
def handlers_index():
    """Retrieves all handlers from data store and returns a JSON array response object."""
    session = get_session()
    query = session.query(Handler)
    handlers = query.all()

    return jsonify([json(handler) for handler in handlers])
