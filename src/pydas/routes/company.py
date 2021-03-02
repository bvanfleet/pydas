from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, request
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Company, Feature, Option

from pydas import constants
from pydas.containers import ApplicationContainer

company_bp = Blueprint('companies',
                       'pydas.routes.companies',
                       url_prefix='/api/v1/companies')


@company_bp.route(constants.BASE_PATH, methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_POST: scopes.COMPANIES_WRITE},
               current_app,
               request)
@inject
def companies_index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if request.method == constants.HTTP_GET:
        with metadata_context.get_session() as session:
            companies = session.query(Company).all()
            return jsonify([json(company) for company in companies])

    request_company = request.get_json()
    with metadata_context.get_session() as session:
        new_company = Company(symbol=request_company['symbol'],
                              name=request_company['name'],
                              market=request_company['market'])
        session.add(new_company)

    return jsonify(json(new_company)), 201


@company_bp.route('/<company_symbol>',
                  methods=[constants.HTTP_GET, constants.HTTP_PATCH, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_PATCH: scopes.COMPANIES_WRITE,
                constants.HTTP_DELETE: scopes.COMPANIES_DELETE},
               current_app,
               request)
@inject
def get_company(company_symbol: str,
                metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            company = session.query(Company).filter(
                Company.symbol == company_symbol).one()
            if request.method == constants.HTTP_GET:
                return jsonify(json(company))

            if request.method == constants.HTTP_DELETE:
                session.delete(company)
                return '', 204

            request_company = request.get_json()
            if request_company['symbol'] != company.symbol:
                return make_response(
                    'Error: Request body does not match the company referenced', 400)

            company.symbol = request_company['symbol']
            company.name = request_company['name']
            company.market = request_company['market']
            session.add(company)
            return jsonify(json(company))
    except NoResultFound:
        response = make_response(
            'Cannot find company requested', 404)
        return response


@company_bp.route('/<company_symbol>/features', methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_POST: scopes.COMPANIES_WRITE},
               current_app,
               request)
@inject
def company_features_index(company_symbol: str,
                           metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            company = session.query(Company).filter(
                Company.symbol == company_symbol).one()

            if request.method == constants.HTTP_GET:
                return jsonify([json(feature) for feature in company.features])

            request_map = request.get_json()
            feature = session.query(Feature).filter(
                Feature.name == request_map['name']).one()
            company.features.append(feature)
            session.add(company)

            return jsonify([json(feature) for feature in company.features]), 201
    except NoResultFound:
        response = make_response(
            'Cannot find company or feature requested', 404)
        return response


@company_bp.route('/<company_symbol>/features/<feature_name>',
                  methods=[constants.HTTP_GET, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_DELETE: scopes.COMPANIES_DELETE},
               current_app,
               request)
@inject
def company_feature_index(company_symbol: str,
                          feature_name: str,
                          metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            company = session.query(Company).filter(
                Company.symbol == company_symbol).one()

            if request.method == constants.HTTP_DELETE:
                feature = session.query(Feature).filter(
                    Feature.name == feature_name).one()
                company.features.remove(feature)
                session.add(company)
                return '', 204

            for feature in company.features:
                if feature.name == feature_name:
                    return jsonify(json(feature))

            response = make_response('Cannot find feature requested', 404)
            return response
    except NoResultFound:
        response = make_response(
            'Cannot find company or feature requested', 404)
        return response


@company_bp.route('/<company_symbol>/features/<feature_name>/options',
                  methods=[constants.HTTP_GET, constants.HTTP_POST])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_POST: scopes.COMPANIES_WRITE},
               current_app,
               request)
@inject
def options_index(company_symbol: str,
                  feature_name: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if request.method == constants.HTTP_GET:
        with metadata_context.get_session() as session:
            query = session.query(Option).filter(
                Option.company_symbol == company_symbol,
                Option.feature_name == feature_name)
            options = query.all()

        return jsonify([json(option) for option in options])

    request_option = request.get_json()

    option_value = (request_option['value_text']
                    if 'value_text' in request_option
                    else request_option['value'])
    with metadata_context.get_session() as session:
        new_option = Option(name=request_option['name'],
                            company_symbol=request_option['company_symbol'],
                            feature_name=request_option['feature_name'],
                            option_type=request_option['option_type'],
                            value_text=option_value,
                            value_number=request_option['value_number'])
        session.add(new_option)

    return jsonify(json(new_option)), 201


@company_bp.route('/<company_symbol>/features/<feature_name>/options/<option_name>',
                  methods=[constants.HTTP_GET, constants.HTTP_PATCH, constants.HTTP_DELETE])
@verify_scopes({constants.HTTP_GET: scopes.COMPANIES_READ,
                constants.HTTP_PATCH: scopes.COMPANIES_WRITE,
                constants.HTTP_DELETE: scopes.COMPANIES_DELETE},
               current_app,
               request)
@inject
def option_index(company_symbol: str,
                 feature_name: str,
                 option_name: str,
                 metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            query = session.query(Option).filter(
                Option.company_symbol == company_symbol,
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
            company_symbol = request_option['company_symbol']
            feature_name = request_option['feature_name']
            option.option_type = request_option['option_type']
            option.value_text = option_value
            option.value_number = request_option['value_number']
            session.add(option)

            return jsonify(json(option))
    except NoResultFound:
        response = make_response('Cannot find option requested', 404)
        return response
