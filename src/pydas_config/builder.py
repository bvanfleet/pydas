"""
Provides a builder method for creating a master configuration object using multiple files and
command-line arguments.
"""

from pydas_config.section import ConfigSection


def build_config(filenames: list, skip_args: bool = False) -> ConfigSection:
    master_config = ConfigSection(None)
    for filename in filenames:
        master_config.update(ConfigSection(filename))

    if not skip_args:
        master_config.update(ConfigSection('args'))

    return master_config
