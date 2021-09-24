"""
pyDAS platform configuration and installation framework. Provides a configuration proxy object that
maps to optional configuration files and/or command-line arguments. This configuration object can
then be used during installation or server execution.
"""
from .builder import build_config
from .schema import validate_schema, ValidationError
from .config import Configuration

__version__ = '0.1.0'
