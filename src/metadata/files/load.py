import json
import logging
from os import path

from jsonschema import validate
from sqlalchemy.sql import exists

from metadata import models as m
from metadata.contexts.base import BaseContext


def load_metadata(config_path: str, context: BaseContext):
    '''
    Loads a config.json file containing metadata into a data context.

    Parameters
    ----------
    config_path: str
      Filepath to the metadata configuration to be loaded.

    context: BaseContext
      Datastore context to load metadata into
    '''
    schema_directory = path.dirname(__file__)
    schema_name = "schema.json"
    schema_path = path.join(schema_directory, schema_name)

    with open(schema_path) as raw_schema:
        schema = json.loads(raw_schema.read())

    session_maker = context.get_session_maker()
    session = session_maker()

    logging.debug('Loading metadata configuration file at %s', config_path)
    with open(config_path) as raw_config:
        config = json.loads(raw_config.read())
        logging.debug('Validating metadata configuration file structure')
        validate(config, schema)

        logging.debug('Loading configuration')
        _load_config(config, session)

        logging.debug('Loading features')
        _load_features(config, session)

        logging.debug('Loading companies')
        _load_companies(config, session)

        logging.debug('Loading feature options')
        _load_feature_options(config, session)

        logging.debug('Metadata configuration file loaded into data store!')


def _load_config(metadata, session):
    next_id = session.query(m.Configuration).count() + 1
    key = m.Configuration(id=next_id,
                          name='api_key',
                          type='str',
                          value_text=metadata['api_key'])
    next_id += 1
    session.add(key)
    logging.debug('Loaded API key!')

    # TODO: Consider if we should track the API version and URI

    output = metadata['output']
    raw_output_format: str = output['format']
    output_format = m.Configuration(id=next_id,
                                    name='outputFormat',
                                    type='str',
                                    value_text=raw_output_format)
    next_id += 1
    session.add(output_format)
    logging.debug('Loaded output format "%s"!', raw_output_format)

    output_prefix = 'output%s' % raw_output_format.capitalize()
    for key, value in output['properties'].items():
        property_name = '{prefix}{name}'.format(prefix=output_prefix,
                                                name=key)
        prop = m.Configuration(id=next_id,
                               name=property_name,
                               type='str',
                               value_text=value)
        next_id += 1
        session.add(prop)
        logging.debug('Loaded output configuration "%s"!', property_name)

    session.commit()


def _load_features(metadata, session):
    for feature_meta in metadata['features']:
        handler_name = feature_meta['handler']
        handler_filter = exists().where(m.Handler.name == handler_name)
        handlers = session.query(m.Handler).filter(handler_filter)
        if handlers.count() == 0:
            next_handler_id = session.query(m.Handler).count() + 1
            handler = m.Handler(id=next_handler_id,
                                name=handler_name)
            session.add(handler)
            session.commit()
            logging.debug('Added handler "%s"!', handler.name)

        handler_id = handlers.first().id
        description = feature_meta['description'] if 'description' in feature_meta else None
        feature = m.Feature(name=feature_meta['name'],
                            uri=feature_meta['uri'],
                            handler_id=handler_id,
                            description=description)
        session.add(feature)
        session.commit()
        logging.debug('Added feature "%s"!', feature.name)


def _load_companies(metadata, session):
    features = session.query(m.Feature).all()
    for symbol in metadata['symbols']:
        company = m.Company(symbol=symbol)
        for feature in features:
            company.features.append(feature)
            logging.debug('Mapping feature "%s" to company with symbol "%s"',
                          feature.name,
                          company.symbol)

        session.add(company)
        session.commit()
        logging.debug('Added company with symbol "%s"', company.symbol)


def _load_feature_options(metadata, session):
    for company in session.query(m.Company).all():
        for feature in company.features:
            features = filter(lambda feature_meta: feature_meta['name'] == feature.name,
                              metadata['features'])

            for mapped_feature in features:
                for option in mapped_feature['options']:
                    option = m.Option(name=option['name'],
                                      value_text=option['value'],
                                      option_type='str',
                                      feature_name=feature.name,
                                      company_symbol=company.symbol)
                    session.add(option)
                    session.commit()
