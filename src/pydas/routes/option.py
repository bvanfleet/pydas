from flask import Blueprint, current_app, request, make_response
from flask.json import jsonify

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Option

from pydas import constants, scopes
from pydas.containers import metadata_container
from pydas.routes.utils import verify_scopes

option_bp = Blueprint('options',
                      'pydas.routes.option',
                      url_prefix='/api/v1/options')


@option_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.OPTIONS_READ,
                constants.HTTP_POST: scopes.OPTIONS_WRITE})
def index():
    metadata_context: BaseContext = metadata_container.context_factory(
        current_app.config['DB_DIALECT'], **current_app.config['DB_CONFIG'])
    session_maker = metadata_context.get_session_maker()
    session = session_maker()

    if request.method == constants.HTTP_GET:
        query = session.query(Option)
        options = query.all()

        return jsonify([json(option) for option in options])

    request_option = request.get_json()

    new_option = Option(name=request_option['name'],
                        company_symbol=request_option['company_symbol'],
                        feature_name=request_option['feature_name'],
                        option_type=request_option['option_type'],
                        value_text=request_option['value_text'],
                        value_number=request_option['value_number'])
    session.add(new_option)
    session.commit()

    return jsonify(json(new_option)), 201


@option_bp.route('/<option_name>', methods=[constants.HTTP_GET])
@verify_scopes({constants.HTTP_GET: scopes.OPTIONS_READ})
def option_index(option_name):
    metadata_context: BaseContext = metadata_container.context_factory(
        current_app.config['DB_DIALECT'], **current_app.config['DB_CONFIG'])
    session_maker = metadata_context.get_session_maker()
    session = session_maker()

    query = session.query(Option).filter(Option.name == option_name)
    options = query.all()
    if options:
        return jsonify([json(option) for option in options])

    response = make_response('Cannot find option requested', 404)
    return response
