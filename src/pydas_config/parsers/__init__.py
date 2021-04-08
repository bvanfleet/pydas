"""
Provides various parsers for obtaining consistent configuration from different sources.
"""

from .argument import ArgumentParser
from .base import BaseParser
from .ini import IniParser
from .yaml import YamlParser


def get_parser(parser_type: str = "args") -> BaseParser:
    """Returns the appropriate parser for the given type.

    Parameters
    ----------
    parser_type: "args" | "yaml" | "ini"
        Parser type being requested
    """
    if parser_type == "args":
        return ArgumentParser

    if parser_type == "yaml":
        return YamlParser

    if parser_type == "ini":
        return IniParser

    raise TypeError(f"Unsupported parser type '{parser_type}' requested!")
