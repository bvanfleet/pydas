from logging.config import dictConfig
from dependency_injector import containers, providers

from pydas_metadata import MetadataContainer


class ConfigContainer(containers.DeclarativeContainer):
    """Provides configuration dependency injection."""
    config = providers.Configuration()

    configure_logging = providers.Resource(dictConfig,
                                           config=config.logging)


metadata_container = MetadataContainer()
config_container = ConfigContainer()
