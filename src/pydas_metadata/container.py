from dependency_injector import containers, providers

from pydas_metadata import contexts


class MetadataContainer(containers.DeclarativeContainer):
    """
    Provides dependency injection support for metadata contexts.

    Attributes
    ----------
    context_factory: :class:`dependency_injector.providers.Factory`
        Factory provider for metadata contexts.

    Example
    -------

    >>> from pydas_metadata import MetadataContainer
    >>> metadata_container = MetadataContainer()
    >>> context = metadata_container.context_factory('sqlite')
    """
    context_factory = providers.Factory(contexts.ContextFactory.get_context)
