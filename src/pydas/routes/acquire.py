from datetime import datetime
from functools import reduce
import logging
from typing import Any

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, make_response, jsonify, request, send_file
from sqlalchemy.orm.exc import NoResultFound

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Company, Configuration, FeatureToggle, Option

from pydas import constants, scopes
from pydas.routes.utils import verify_scopes
from pydas.signals import SignalFactory
from pydas.clients.iex import IexClient
from pydas.constants import FeatureToggles
from pydas.containers import ApplicationContainer
from pydas.formatters import BaseFormatter, FormatterFactory

# Disable the call to current_app._get_current_object as it's recommended by Flask
# pylint: disable=protected-access

acquire_bp = Blueprint('acquire',
                       'pydas.routes.acquire',
                       url_prefix='/api/v1/acquire')
"""
An acquisition blueprint that defines how the sDAS API provides REST
functionality for dataset generation.
"""


@acquire_bp.route('/<company_symbol>', methods=[constants.HTTP_GET])
@verify_scopes({constants.HTTP_GET: scopes.ACQUIRE_READ})
@inject
def acquire(company_symbol,
            metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]):
    """
    Provides API function for dataset generation.

    Parameters
    ----------
    company_symbol: str
        Symbol for the company to acquire data for.

    Returns
    -------
    flask.Response:
        HTTP response with dataset as a JSON payload or delimited file.
        This is determined from whether a query parameter is provided
        that specifies a file output formatter.

    Raises
    ------
    sqlalchemy.exc.OperationalError:
        Thrown if there is an issue communicating with the metadata database.
    """
    session = metadata_context.get_session()

    query = session.query(Company).filter(Company.symbol == company_symbol)
    event_handler = session.query(FeatureToggle).filter(
        FeatureToggle.name == FeatureToggles.event_handlers).one_or_none()
    if event_handler.is_enabled is True:
        logging.info("Signalling pre-acquisition event handlers")
        SignalFactory.pre_acquisition.send(
            company_symbol=company_symbol,
            start_date=datetime.now().isoformat())

    results = {}

    api_key = session.query(Configuration).filter(
        Configuration.name == 'apiKey').one()
    logging.debug("Creating IEX client with API Key: %s",
                  api_key.value_text)
    client = IexClient(api_key.value_text)

    try:
        if event_handler.is_enabled is True:
            logging.info("Signalling pre-company event handlers")
            SignalFactory.pre_company.send(
                company_symbol=company_symbol,
                start_date=datetime.now().isoformat())

        company = query.one()
        for feature in company.features:
            if event_handler.is_enabled is True:
                logging.info(
                    "Signalling pre-feature event handlers")
                SignalFactory.pre_feature.send(
                    company_symbol=company.symbol,
                    feature_name=feature.name,
                    start_date=datetime.now().isoformat())

            feature_option = session.query(Option).filter(Option.company_symbol == company.symbol,
                                                          Option.feature_name == feature.name).all()
            option = [json(option) for option in feature_option]
            logging.info(
                'Retrieved mapped options: [%s]',
                (" ").join([json(option, True) for option in feature_option]))

            # TODO: Determine if this could/should be moved into source-aware code
            if feature.handler_meta.name == "tech_indicators_handler" and not option:
                logging.info(
                    'Adding missing option on technical indicator')
                option.append({"feature_name": feature.name,
                               "name": "range",
                               "value": "1m"})

            logging.info('Acquiring feature data')
            data = client.get_feature_data(feature, company, option)
            if isinstance(data, list):
                results[feature.name] = feature.get_values(data)
            elif isinstance(data, dict):
                results[feature.name] = [feature.get_value(data)]
            logging.info(
                "Acquired %d rows", len(results[feature.name]))

            if event_handler.is_enabled is True:
                logging.info(
                    "Signalling post-feature event handlers")
                SignalFactory.post_feature.send(
                    company_symbol=company.symbol,
                    feature_name=feature.name,
                    feature_rows=len(results[feature.name]),
                    end_date=datetime.now().isoformat())

        logging.info("Transforming results info JSON structure")
        formatter: BaseFormatter = FormatterFactory.get_formatter('json')
        results = formatter.transform(results)
        if event_handler.is_enabled is True:
            logging.info("Signalling post-company event handlers")
            count = reduce(lambda total, iter: total + len(iter),
                           results['values'],
                           0)
            SignalFactory.post_company.send(
                company_symbol=company.symbol,
                data=results,
                total_rows=count,
                end_date=datetime.now().isoformat())

        format_options = request.args
        format_options_dict = {}
        if 'format' in format_options:
            logging.info('Applying additional output formatting with type %s',
                         format_options['format'])
            output_format = request.args['format']

            format_options_dict['output_path'] = __get_output_configuration(
                {}, '', 'OutputFilePath', session)
            if format_options_dict['output_path'] is None:
                raise ValueError('Error: The output file path is not set!')

            format_options_dict['row_delimiter'] = __get_output_configuration(
                format_options,
                'rowDelimiter',
                'OutputFileRowDelimiter',
                session)

            format_options_dict['field_delimiter'] = __get_output_configuration(
                format_options,
                'fieldDelimiter',
                'OutputFileFieldDelimiter',
                session)

            format_options_dict['include_headers'] = __get_output_configuration(
                format_options,
                'header',
                'OutputFileHasHeaderRow',
                session)
            try:
                logging.info("Transforming result set and saving to %s",
                             format_options_dict['output_path'])
                formatter = FormatterFactory.get_formatter(output_format)
                format_result = formatter.transform(
                    results, **format_options_dict)
            except Exception as exc:
                response = make_response(str(exc), 400)
                return response

            if output_format.lower() == 'file':
                if event_handler.is_enabled is True:
                    logging.info(
                        "Signalling post-acquisition event handlers")
                    SignalFactory.post_acquisition.send(
                        company_symbol=company.symbol,
                        end_date=datetime.now().isoformat(),
                        message='Completed data acquisition!',
                        uri=request.path,
                        type='INFO')

                return send_file(format_result, as_attachment=True, cache_timeout=0)

        if event_handler.is_enabled is True:
            logging.info(
                "Signalling post-acquisition event handlers")
            SignalFactory.post_acquisition.send(
                company_symbol=company.symbol,
                end_date=datetime.now().isoformat(),
                message='Completed data acquisition!',
                uri=request.path,
                type='INFO')

        return jsonify(results)
    except NoResultFound:
        response = make_response(
            'Cannot find company', 404)
        return response


def __get_output_configuration(config: dict, attribute: str, option: str, session) -> Any:
    if attribute in config:
        return config[attribute]
    else:
        try:
            attribute = session.query(Configuration).filter(
                Configuration.name == option).one()
            return attribute.value
        except NoResultFound:
            return ''
