from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, request
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Entity, Feature, Option

from pydas import constants
from pydas.containers import ApplicationContainer

entity_bp = Blueprint('entities',
                       'pydas.routes.entities',
                       url_prefix='/api/v1/entities')


@entity_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_POST: scopes.COMPANIES_WRITE},
               current_app,
               request)
@inject
def entities_index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if request.method == constants.HTTP_GET:
        with metadata_context.get_session() as session:
            entities = session.query(Entity).all()
            return jsonify([json(entity) for entity in entities])

    request_entity = request.get_json()
    with metadata_context.get_session() as session:
        new_entity = Entity(identifier=request_entity['identifier'],
                             name=request_entity['name'],
                             category=request_entity['category'])
        session.add(new_entity)

    return jsonify(json(new_entity)), 201


@entity_bp.route('/<entity_identifier>',
                  methods=[constants.HTTP_GET, constants.HTTP_PATCH, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_PATCH: scopes.COMPANIES_WRITE,
                constants.HTTP_DELETE: scopes.COMPANIES_DELETE},
               current_app,
               request)
@inject
def get_entity(entity_identifier: str,
                metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            entity = session.query(Entity).filter(
                Entity.identifier == entity_identifier).one()
            if request.method == constants.HTTP_GET:
                return jsonify(json(entity))

            if request.method == constants.HTTP_DELETE:
                session.delete(entity)
                return '', 204

            request_entity = request.get_json()
            if request_entity['identifier'] != entity.identifier:
                return make_response(
                    'Error: Request body does not match the entity referenced', 400)

            entity.identifier = request_entity['identifier']
            entity.name = request_entity['name']
            entity.category = request_entity['category']
            session.add(entity)
            return jsonify(json(entity))
    except NoResultFound:
        response = make_response(
            'Cannot find the entity requested', 404)
        return response


@entity_bp.route('/<entity_identifier>/features', methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_POST: scopes.COMPANIES_WRITE},
               current_app,
               request)
@inject
def entity_features_index(entity_identifier: str,
                           metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            entity = session.query(Entity).filter(
                Entity.identifier == entity_identifier).one()

            if request.method == constants.HTTP_GET:
                return jsonify([json(feature) for feature in entity.features])

            request_map = request.get_json()
            feature = session.query(Feature).filter(
                Feature.name == request_map['name']).one()
            entity.features.append(feature)
            session.add(entity)

            return jsonify([json(feature) for feature in entity.features]), 201
    except NoResultFound:
        response = make_response(
            'Cannot find the entity or feature requested', 404)
        return response


@entity_bp.route('/<entity_identifier>/features/<feature_name>',
                  methods=[constants.HTTP_GET, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_DELETE: scopes.COMPANIES_DELETE},
               current_app,
               request)
@inject
def entity_feature_index(entity_identifier: str,
                          feature_name: str,
                          metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            entity = session.query(Entity).filter(
                Entity.identifier == entity_identifier).one()

            if request.method == constants.HTTP_DELETE:
                feature = session.query(Feature).filter(
                    Feature.name == feature_name).one()
                entity.features.remove(feature)
                session.add(entity)
                return '', 204

            for feature in entity.features:
                if feature.name == feature_name:
                    return jsonify(json(feature))

            response = make_response('Cannot find feature requested', 404)
            return response
    except NoResultFound:
        response = make_response(
            'Cannot find the entity or feature requested', 404)
        return response


@entity_bp.route('/<entity_identifier>/features/<feature_name>/options',
                  methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_POST: scopes.COMPANIES_WRITE},
               current_app,
               request)
@inject
def options_index(entity_identifier: str,
                  feature_name: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if request.method == constants.HTTP_GET:
        with metadata_context.get_session() as session:
            query = session.query(Option).filter(
                Option.entity_identifier == entity_identifier,
                Option.feature_name == feature_name)
            options = query.all()

        return jsonify([json(option) for option in options])

    request_option = request.get_json()

    option_value = (request_option['value_text']
                    if 'value_text' in request_option
                    else request_option['value'])
    with metadata_context.get_session() as session:
        new_option = Option(name=request_option['name'],
                            entity_identifier=request_option['entity_identifier'],
                            feature_name=request_option['feature_name'],
                            option_type=request_option['option_type'],
                            value_text=option_value,
                            value_number=request_option['value_number'])
        session.add(new_option)

    return jsonify(json(new_option)), 201


@entity_bp.route('/<entity_identifier>/features/<feature_name>/options/<option_name>',
                  methods=[constants.HTTP_GET, constants.HTTP_PATCH, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_PATCH: scopes.COMPANIES_WRITE,
                constants.HTTP_DELETE: scopes.COMPANIES_DELETE},
               current_app,
               request)
@inject
def option_index(entity_identifier: str,
                 feature_name: str,
                 option_name: str,
                 metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            query = session.query(Option).filter(
                Option.entity_identifier == entity_identifier,
                Option.feature_name == feature_name,
                Option.name == option_name)
            option = query.one()
            if request.method == constants.HTTP_GET:
                return jsonify(json(option))

            if request.method == constants.HTTP_DELETE:
                session.delete(option)
                return '', 204

            request_option = request.get_json()
            if request_option['name'] != option.name:
                return make_response(
                    'Error: Request body does not match the option referenced', 400)

            option_value = (request_option['value_text']
                            if 'value_text' in request_option
                            else request_option['value'])
            entity_identifier = request_option['entity_identifier']
            feature_name = request_option['feature_name']
            option.option_type = request_option['option_type']
            option.value_text = option_value
            option.value_number = request_option['value_number']
            session.add(option)

            return jsonify(json(option))
    except NoResultFound:
        response = make_response('Cannot find option requested', 404)
        return response
