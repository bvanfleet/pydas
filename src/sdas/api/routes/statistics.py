from flask import Blueprint, make_response
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import func

from metadata import json
from metadata.models import Statistics

from sdas.api import constants
from sdas.api import scopes
from sdas.api.routes.utils import get_session, verify_scopes

statistics_bp = Blueprint('statistics',
                          'sdas.api.routes.statistics',
                          url_prefix='/api/v1/statistics')


@statistics_bp.route(constants.BASE_PATH)
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ})
def index():
    session = get_session()

    query = session.query(Statistics)
    statistics = query.all()

    return jsonify([json(entry) for entry in statistics])


@statistics_bp.route('/company/<company_symbol>')
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ})
def company_index(company_symbol):
    session = get_session()

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
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ})
def feature_index(company_symbol):
    session = get_session()

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
@verify_scopes({constants.HTTP_GET: scopes.STATISTICS_READ})
def feature_stats(company_symbol, feature_name):
    session = get_session()

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

    try:
        statistics = query.one()
    except NoResultFound:
        response = make_response(
            'Cannot find feature requested', 404)
        return response

    return jsonify({
        "company_symbol": statistics.company_symbol,
        "feature_name": statistics.feature_name,
        "total_row_count": int(statistics.row_count)
    })
