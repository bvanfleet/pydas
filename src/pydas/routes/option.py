from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, request
from flask.json import jsonify

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Option

from pydas import constants
from pydas.containers import ApplicationContainer

option_bp = Blueprint('options',
                      'pydas.routes.option',
                      url_prefix='/api/v1/options')


@option_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.OPTIONS_READ,
                constants.HTTP_POST: scopes.OPTIONS_WRITE},
               current_app,
               request)
@inject
def index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if request.method == constants.HTTP_GET:
        with metadata_context.get_session() as session:
            options = session.query(Option).all()
            return jsonify([json(option) for option in options])

    with metadata_context.get_session() as session:
        request_option = request.get_json()
        new_option = Option(name=request_option['name'],
                            company_symbol=request_option['company_symbol'],
                            feature_name=request_option['feature_name'],
                            option_type=request_option['option_type'],
                            value_text=request_option['value_text'],
                            value_number=request_option['value_number'])
        session.add(new_option)

        return jsonify(json(new_option)), 201


@option_bp.route('/<option_name>', methods=[constants.HTTP_GET])
@verify_scopes({constants.HTTP_GET: scopes.OPTIONS_READ},
               current_app,
               request)
@inject
def option_index(option_name: str,
                 metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    with metadata_context.get_session() as session:
        options = session.query(Option).filter(
            Option.name == option_name).all()
        if options:
            return jsonify([json(option) for option in options])

        response = make_response('Cannot find option requested', 404)
        return response
