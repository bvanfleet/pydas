from flask import Blueprint, request, make_response
from flask.json import jsonify

from metadata import json
from metadata.models import Option

from pydas import constants
from pydas import scopes
from pydas.routes.utils import get_session, verify_scopes

option_bp = Blueprint('options',
                      'pydas.routes.option',
                      url_prefix='/api/v1/options')


@option_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.OPTIONS_READ, constants.HTTP_POST: scopes.OPTIONS_WRITE})
def index():
    session = get_session()

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
    session = get_session()

    query = session.query(Option).filter(Option.name == option_name)
    options = query.all()
    if options:
        return jsonify([json(option) for option in options])

    response = make_response('Cannot find option requested', 404)
    return response
