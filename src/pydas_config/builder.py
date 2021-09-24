"""
Provides a builder method for creating a master configuration object using multiple files and
command-line arguments.
"""

from pydas_config.config import Configuration


def build_config(*filenames, skip_args: bool = False) -> Configuration:
    """
    Builds a configuration from an ordered list of files and command-line arguments. When building
    the configuration, the files are parsed first and finally updated with command-line args.

    Parameters
    ----------
    filenames: tuple[str]
        Collection of files to be parsed. Files are parsed in the order that they are passed in to
        the function. Files parsed later may overwrite existing configuration values.

    skip_args: bool
        Flag indicating whether the function should skip parsing command-line arguments after the
        files have been processed. Defaults to False.

    Returns
    -------
    :class:`pydas_config.Configuration`
        Configuration object that has been updated with all configuration files and (optionally)
        command-line arguments.
    """

    master_config = Configuration(None)
    for filename in filenames:
        master_config.update(Configuration(filename))

    if not skip_args:
        master_config.update(Configuration('args'))

    return master_config
