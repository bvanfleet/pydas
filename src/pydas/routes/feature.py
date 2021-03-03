from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, request, make_response
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Feature, Handler

from pydas import constants
from pydas.containers import ApplicationContainer

feature_bp = Blueprint('features',
                       'pydas.routes.feature',
                       url_prefix='/api/v1/features')


@feature_bp.route(constants.BASE_PATH,
                  methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.FEATURES_READ,
                constants.HTTP_POST: scopes.FEATURES_WRITE},
               current_app,
               request)
@inject
def index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    """Handler for base level URI for the features endpoint.
    Supports GET and POST methods for interacting."""
    if request.method == constants.HTTP_GET:
        with metadata_context.get_session() as session:
            features = session.query(Feature).all()
            return jsonify([json(feature) for feature in features])

    with metadata_context.get_session() as session:
        request_feature = request.get_json()
        handler = session.query(Handler).filter(
            Handler.id == request_feature['handler']['id']).one()

        new_feature = Feature(name=request_feature['name'],
                              uri=request_feature['uri'],
                              description=request_feature['description'],
                              handler_metadata=handler)
        session.add(new_feature)

        return jsonify(json(new_feature)), 201


@feature_bp.route('/<feature_name>',
                  methods=[constants.HTTP_GET, constants.HTTP_PATCH, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.FEATURES_READ,
                constants.HTTP_PATCH: scopes.FEATURES_WRITE,
                constants.HTTP_DELETE: scopes.FEATURES_DELETE},
               current_app,
               request)
@inject
def feature_index(feature_name: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    """Handler for individual feature level URI of the features endpoint.
    Supports GET, PATCH, and DELETE methods for interacting."""
    try:
        with metadata_context.get_session() as session:
            feature = session.query(Feature).filter(
                Feature.name == feature_name).one()
            if request.method == constants.HTTP_GET:
                return jsonify(json(feature))

            if request.method == constants.HTTP_DELETE:
                session.delete(feature)
                return '', 204

            request_feature = request.get_json()
            if request_feature['name'] != feature.name:
                return make_response('Error: Request body does not match the feature referenced', 400)

            handler = session.query(Handler).filter(
                Handler.id == request_feature['handler']['id']).one()
            feature.description = request_feature['description']
            feature.uri = request_feature['uri']
            feature.handler_metadata = handler
            session.add(feature)

            return jsonify(json(feature))
    except NoResultFound:
        response = make_response(
            'Cannot find feature requested', 404)
        return response
