from dependency_injector import containers, providers

from pydas_metadata import MetadataContainer


class ConfigContainer(containers.Container):
    """Provides configuration dependency injection."""
    config = providers.Configuration()


metadata_container = MetadataContainer()
config_container = ConfigContainer()
