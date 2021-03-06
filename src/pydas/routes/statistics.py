from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, request
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import func

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Statistics

from pydas import constants
from pydas.containers import ApplicationContainer

statistics_bp = Blueprint('statistics',
                          'pydas.routes.statistics',
                          url_prefix='/api/v1/statistics')


@statistics_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ},
               current_app,
               request)
@inject
def index(metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    with metadata_context.get_session() as session:
        statistics = session.query(Statistics).all()
        return jsonify([json(entry) for entry in statistics])


@statistics_bp.route('/company/<company_symbol>')
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ},
               current_app,
               request)
def company_index(company_symbol: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    with metadata_context.get_session() as session:
        query = session.query(
            Statistics.company_symbol,
            func.sum(Statistics.row_count).label("row_count")
        ).filter(
            Statistics.company_symbol == company_symbol
        ).group_by(
            Statistics.company_symbol)

        try:
            statistics = query.one()
        except NoResultFound:
            response = make_response(
                'Cannot find company requested', 404)
            return response

        return jsonify({
            "company_symbol": statistics.company_symbol,
            "total_row_count": int(statistics.row_count)
        })


@statistics_bp.route('/company/<company_symbol>/features')
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ},
               current_app,
               request)
@inject
def feature_index(company_symbol: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    with metadata_context.get_session() as session:
        query = session.query(
            Statistics.company_symbol,
            Statistics.feature_name,
            func.sum(Statistics.row_count).label("row_count")
        ).filter(
            Statistics.company_symbol == company_symbol
        ).group_by(
            Statistics.company_symbol,
            Statistics.feature_name)
        statistics = query.all()

        return jsonify([{
            "company_symbol": entry.company_symbol,
            "feature_name": entry.feature_name,
            "total_row_count": int(entry.row_count)
        } for entry in statistics])


@statistics_bp.route('/company/<company_symbol>/features/<feature_name>')
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ},
               current_app,
               request)
@inject
def feature_stats(company_symbol: str,
                  feature_name: str,
                  metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    try:
        with metadata_context.get_session() as session:
            query = session.query(
                Statistics.company_symbol,
                Statistics.feature_name,
                func.sum(Statistics.row_count).label("row_count")
            ).filter(
                Statistics.company_symbol == company_symbol,
                Statistics.feature_name == feature_name
            ).group_by(
                Statistics.company_symbol,
                Statistics.feature_name)

            statistics = query.one()
            return jsonify({
                "company_symbol": statistics.company_symbol,
                "feature_name": statistics.feature_name,
                "total_row_count": int(statistics.row_count)
            })
    except NoResultFound:
        response = make_response(
            'Cannot find feature requested', 404)
        return response
