import logging
import logging.config
from metadata import contexts
from metadata import models
from metadata.files import load_metadata
from sdas.constants import SdasConstants
from sdas.formatters import BaseFormatter, FormatterFactory


class MockCompany():
    def __init__(self, symbol):
        self.symbol = symbol


def retrieve_data(features: list, symbol: str, apiKey: str):
    from sdas.feature_mapper.feature_map import FeatureMap
    from sdas.clients.iex import IexClient
    from metadata.contexts import DatabaseContext

    context = DatabaseContext('sdasadmin', 'root')
    session_maker = context.get_session_maker()
    session = session_maker()

    logging.info('Retrieving data for "%s"...', symbol)
    results = {}
    for feature in features:
        logging.debug('Retrieving metadata for feature "%s"...',
                      feature['name'])
        mapper = FeatureMap()
        options = feature['options'] if 'options' in feature else []
        feature_meta = mapper.get_feature(
            feature[SdasConstants.name_property],
            symbol,
            options)
        if feature_meta is None:
            logging.warning(
                'Feature "%s" isn''t currently mapped. No data will be available for this feature. Contact the developer for further assistance',
                features)
            continue

        if feature_meta.name in FeatureMap.technical_indicators(session):
            feature_meta.options.append({"feature_name": feature_meta.name})

        client = IexClient(apiKey)
        data = None
        try:
            logging.debug('Requesting data from IEX Cloud...')
            logging.info('Retrieving feature data "%s"...', feature_meta.name)
            data = client.get_feature_data(
                feature_meta, MockCompany(symbol), options)
            logging.info('Data retrieved for feature "%s"!', feature_meta.name)
        except Exception as ex:
            logging.error(
                'Unable to retrieve feature %s for symbol "%s":  (%s) %s',
                feature_meta.name,
                symbol,
                type(ex),
                ex,
                stack_info=True)
            continue

        if isinstance(data, list):
            results[feature_meta.name] = feature_meta.get_values(data)
        elif isinstance(data, dict):
            results[feature_meta.name] = [feature_meta.get_value(data)]
        else:
            logging.warning(
                'No data retrieved for feature "%s"',
                feature_meta.name)

    return results


def write_to_output(session, symbol: str, data: dict):
    format = session.query(models.Configuration).filter(
        models.Configuration == 'outputFormat').first()
    logging.info(
        'Writing data for "%s" to "%s"...',
        symbol,
        format)

    if format == 'file':
        file_config = session.query(models.Configuration).filter(
            models.Configuration.name.ilike('outputFile%')).all()
        field_delimiter = ','
        row_delimiter = '\n'
        for config in file_config:
            if config.name == 'outputFileFieldDelimiter':
                field_delimiter = config.value_text
            elif config.name == 'outputFileRowDelimiter':
                row_delimiter = config.value_text

        formatter: BaseFormatter = FormatterFactory.get_formatter('json')
        master_data = formatter.transform(data)

        try:
            with open(f'{symbol}_data.csv', "w") as file:
                logging.debug('Writing data rows...')
                has_headers = session.query(models.Option).filter(
                    models.Option.name == 'outputFileHasHeaderRow').first()
                if has_headers.value_text in ['True', 'true']:
                    logging.debug('Writing header row...')
                    file.write(field_delimiter.join(
                        master_data[SdasConstants.header_property]) + '\n')

                for row in master_data[SdasConstants.multi_value_property]:
                    file.write(field_delimiter.join(
                        map(str, row)) + row_delimiter)
        except OSError as ex:
            logging.error(
                'Unable to write to file: (%s) %s',
                type(ex),
                ex,
                stack_info=True)
            return

    logging.info('Data written successfully!')


if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} <config path>')
        sys.exit(-1)

    script_path = os.path.realpath(__file__)
    config_path = os.path.join(
        os.path.dirname(script_path),
        'logs.conf'
    )
    logging.config.fileConfig(config_path)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    logging.info('Stock Data Acquisition Service initializing...')
    logging.debug('Logging Initialized')
    logging.debug('Initializing metadata context...')
    context = contexts.MemoryContext()
    models.Base.metadata.create_all(context.engine)
    session_maker = context.get_session_maker()
    session = session_maker()
    logging.debug('Metadata context initialized')
    logging.debug('Loading user configuration...')
    load_metadata(sys.argv[1], context)
    logging.debug('User configuration loaded')
    logging.info('Service initialized!')

    api_key = session.query(models.Configuration).filter(
        models.Configuration.name == 'api_key').first()
    for company in session.query(models.Company).all():
        data = retrieve_data(
            company.features, company.symbol, api_key.value_text)
        if data is not None and len(data.keys()) > 0:
            write_to_output(session, company.symbol, data)
        else:
            logging.debug(
                'Skipping data output as there is no data to be written')

    logging.info('Stock Data Acquisition Service stopping...')
