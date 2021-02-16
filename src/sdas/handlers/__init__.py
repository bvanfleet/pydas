"""
sDAS handler functions for acquiring data from various data sources.

Each handler function follows the general form of:

.. code-block:: python

   def name_handler(uri: str, options: dict, api_key: str) -> list:
     # function logic...


For each handler, the uri is the resource location where the request
should be made. This may be a TCP/UDP URI or a local resource URI,
e.g. CSV file. The options are additional configuration options on
the feature which may control how the handler behaved.

The API key is required for many REST API calls to third-party
services. Although, for flat file handlers, or APIs that don't
implement an API key, this will obviously be an optional parameter.

All handlers should return a list containing all data acquired from
the resource. The list does not enforce any internal data types, so
type validation or processing may be required afterwards.
"""

from .iex_handlers import batch_handler
from .iex_handlers import range_handler
from .iex_handlers import tech_indicators_handler
from .iex_news_handlers import news_handler
