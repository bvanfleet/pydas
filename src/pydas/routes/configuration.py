from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, request
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Configuration

from pydas import constants
from pydas.containers import ApplicationContainer

configuration_bp = Blueprint('configuration',
                             'pydas.routes.configuration',
                             url_prefix='/api/v1/configuration')


@configuration_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.CONFIGURATION_READ},
               current_app,
               request)
@inject
def get_configuration(
        metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    with metadata_context.get_session() as session:
        configurations = session.query(Configuration).all()
        return jsonify([json(configuration) for configuration in configurations])


@configuration_bp.route('/<configuration_name>',
                        methods=[constants.HTTP_GET, constants.HTTP_PATCH])
@verify_scopes({constants.HTTP_GET: scopes.CONFIGURATION_READ,
                constants.HTTP_PATCH: scopes.CONFIGURATION_WRITE},
               current_app,
               request)
@inject
def configuration_index(configuration_name: str,
                        metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    """
    Provides a read-write endpoint for working with a single configuration option.
    """
    try:
        with metadata_context.get_session() as session:
            configuration = session.query(Configuration).filter(
                Configuration.name == configuration_name).one()

            if request.method == constants.HTTP_GET:
                return jsonify(json(configuration))

            # Patch logic
            request_configuration = request.get_json()
            if request_configuration['name'] != configuration.name:
                return make_response('Error: Request body does not match the configuration referenced',
                                     400)

            configuration.type = request_configuration['type']
            configuration.value_text = request_configuration['value_text']
            configuration.value_number = request_configuration['value_number']
            session.add(configuration)

            return jsonify(json(configuration))
    except NoResultFound:
        response = make_response(
            'Cannot find configuration requested', 404)
        return response
