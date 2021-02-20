from flask import Blueprint, request, make_response
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

from pydas_metadata import json
from pydas_metadata.models import Configuration

from pydas import constants
from pydas import scopes
from pydas.routes.utils import get_session, verify_scopes

configuration_bp = Blueprint('configuration',
                             'pydas.routes.configuration',
                             url_prefix='/api/v1/configuration')


@configuration_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.CONFIGURATION_READ})
def get_configuration():
    session = get_session()
    query = session.query(Configuration)
    configurations = query.all()

    return jsonify([json(configuration) for configuration in configurations])


@configuration_bp.route('/<configuration_name>', methods=[constants.HTTP_GET, constants.HTTP_PATCH])
@verify_scopes({constants.HTTP_GET: scopes.CONFIGURATION_READ, constants.HTTP_PATCH: scopes.CONFIGURATION_WRITE})
def configuration_index(configuration_name):
    session = get_session()
    query = session.query(Configuration).filter(
        Configuration.name == configuration_name)

    try:
        configuration = query.one()
        if request.method == constants.HTTP_GET:
            return jsonify(json(configuration))

        # Patch logic
        request_configuration = request.get_json()
        if request_configuration['name'] != configuration.name:
            return make_response('Error: Request body does not match the configuration referenced', 400)

        configuration.type = request_configuration['type']
        configuration.value_text = request_configuration['value_text']
        configuration.value_number = request_configuration['value_number']
        session.add(configuration)
        session.commit()
        return jsonify(json(configuration))
    except NoResultFound:
        response = make_response(
            'Cannot find configuration requested', 404)
        return response
