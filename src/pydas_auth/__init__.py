"""
    Authentication Middleware
    ------------------------

    This module provides pluggable support for authentication against the API.
"""

from . import scopes
from .clients import BaseAuthClient, AuthClientFactory
from .scopes import verify_scopes

__version__ = "0.1.0"
