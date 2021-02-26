from logging.config import dictConfig

from dependency_injector import containers, providers
from flask import Flask

from pydas_metadata import contexts


class ApplicationContainer(containers.DeclarativeContainer):
    """Provides configuration dependency injection."""
    app = providers.Dependency(instance_of=Flask)

    config = providers.Configuration()

    configure_logging = providers.Resource(dictConfig,
                                           config=config.logging)

    context_factory = providers.Factory(contexts.ContextFactory.get_context,
                                        context_type=config.database.dialect,
                                        database=config.database.initial_catalog,
                                        hostname=config.database.hostname,
                                        port=config.database.port,
                                        username=config.database.username)
