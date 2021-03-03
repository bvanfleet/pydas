from datetime import datetime
from functools import reduce
import logging

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, current_app, make_response, jsonify, request, send_file
from sqlalchemy.orm.exc import NoResultFound

from pydas_auth import scopes
from pydas_auth.scopes import verify_scopes

from pydas_metadata import json
from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Company, Option

from pydas import constants
from pydas.clients.iex import IexClient
from pydas.constants import FeatureToggles
from pydas.containers import ApplicationContainer
from pydas.formatters import BaseFormatter, FormatterFactory
from pydas.signals import SignalFactory

# Disable the call to current_app._get_current_object as it's recommended by Flask
# pylint: disable=protected-access

acquire_bp = Blueprint('acquire',
                       'pydas.routes.acquire',
                       url_prefix='/api/v1/acquire')


@acquire_bp.route('/<company_symbol>', methods=[constants.HTTP_GET])
@verify_scopes({constants.HTTP_GET: scopes.ACQUIRE_READ},
               current_app,
               request)
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
    should_handle_events = metadata_context.get_feature_toggle(
        FeatureToggles.event_handlers)

    if should_handle_events:
        logging.info("Signalling pre-acquisition event handlers")
        SignalFactory.pre_acquisition.send(
            company_symbol=company_symbol,
            start_date=datetime.now().isoformat())

    results = dict()
    api_key = metadata_context.get_configuration('apiKey')
    logging.debug("Creating IEX client with API Key: %s", api_key)
    client = IexClient(api_key)

    try:
        if should_handle_events:
            logging.info("Signalling pre-company event handlers")
            SignalFactory.pre_company.send(
                company_symbol=company_symbol,
                start_date=datetime.now().isoformat())

        with metadata_context.get_session() as session:
            company = session.query(Company).filter(
                Company.symbol == company_symbol).one()

            for feature in company.features:
                if should_handle_events:
                    logging.info(
                        "Signalling pre-feature event handlers")
                    SignalFactory.pre_feature.send(
                        company_symbol=company_symbol,
                        feature_name=feature.name,
                        start_date=datetime.now().isoformat())

                feature_option = session.query(Option).filter(Option.company_symbol == company_symbol,
                                                              Option.feature_name == feature.name).all()
                option = [json(option) for option in feature_option]
                logging.info(
                    'Retrieved mapped options: [%s]',
                    (" ").join([json(option, True) for option in feature_option]))

                # TODO: Determine if this could/should be moved into source-aware code
                if feature.handler_metadata.name == "tech_indicators_handler" and not option:
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

                if should_handle_events:
                    logging.info(
                        "Signalling post-feature event handlers")
                    SignalFactory.post_feature.send(
                        company_symbol=company_symbol,
                        feature_name=feature.name,
                        feature_rows=len(results[feature.name]),
                        end_date=datetime.now().isoformat())

        results = __format_output(results, 'json')
        if should_handle_events:
            logging.info("Signalling post-company event handlers")
            count = reduce(lambda total, iter: total + len(iter),
                           results['values'],
                           0)
            SignalFactory.post_company.send(
                company_symbol=company_symbol,
                data=results,
                total_rows=count,
                end_date=datetime.now().isoformat())

        if 'format' in request.args:
            try:
                format_result = __format_output(
                    results, request.args['format'])
            except Exception as exc:
                response = make_response(str(exc), 400)
                return response

            if request.args['format'].lower() == 'file':
                if should_handle_events:
                    logging.info(
                        "Signalling post-acquisition event handlers")
                    SignalFactory.post_acquisition.send(
                        company_symbol=company_symbol,
                        end_date=datetime.now().isoformat(),
                        message='Completed data acquisition!',
                        uri=request.path,
                        type='INFO')

                return send_file(format_result, as_attachment=True, cache_timeout=0)

        if should_handle_events:
            logging.info(
                "Signalling post-acquisition event handlers")
            SignalFactory.post_acquisition.send(
                company_symbol=company_symbol,
                end_date=datetime.now().isoformat(),
                message='Completed data acquisition!',
                uri=request.path,
                type='INFO')

        return jsonify(results)
    except NoResultFound:
        response = make_response('Cannot find company', 404)
        return response


def __format_output(raw_results: dict,
                    format_output: str):
    logging.info('Applying additional output formatting with type %s',
                 format_output)
    formatter: BaseFormatter = FormatterFactory.get_formatter(format_output)
    format_options = dict()

    if format_output == 'file':
        format_options['output_path'] = __get_output_configuration(
            dict(), '', 'OutputFilePath')

        if format_options['output_path'] is None:
            raise ValueError('Error: The output file path is not set!')

        logging.info('Formatted output will be saved to %s',
                     format_options['output_path'])
        format_options['row_delimiter'] = __get_output_configuration(
            format_options,
            'rowDelimiter',
            'OutputFileRowDelimiter')

        format_options['field_delimiter'] = __get_output_configuration(
            format_options,
            'fieldDelimiter',
            'OutputFileFieldDelimiter')

        format_options['include_headers'] = __get_output_configuration(
            format_options,
            'header',
            'OutputFileHasHeaderRow')

    return formatter.transform(raw_results, **format_options)


@inject
def __get_output_configuration(config: dict,
                               attribute: str,
                               option: str,
                               context: BaseContext = Provide[ApplicationContainer.context_factory]):
    if attribute in config:
        return config[attribute]

    config = context.get_configuration(option)
    return '' if config is None else config
