"""
This module provides commonly used functions across the ``sdas.handlers`` module.
"""

import datetime as dt
from calendar import monthrange
from sdas.constants import SdasConstants


def build_query(options: list, key: str) -> str:
    """
    Generates a query string from a given list of :class:`metadata.models.Option`
    objects and an API key.

    Parameters
    ----------
    options: list
        Collection of :class:`metadata.models.Option` objects for building the
        query string.

    key: str
        IEX API key for authenticating HTTP requests.

    Returns
    -------
    str:
        Query string in the format:
        ``?<option_name>=<option_value>[&<option_name>=<option_value>&...]&token=<key>``.
    """
    query = '?'
    for option in options:
        name = option[SdasConstants.name_property]
        value = option[SdasConstants.value_property]
        query += f"{name}={value}&"

    return query + f'token={key}'


def calc_range(start: dt.date, date_range: str):
    """
    Given a date range and starting date, returns the number of days within
    the range. This is useful for IEX range handlers that need to call the
    API for each given day to acquire a range of data points.

    Parameters
    ----------
    start: :class:`datetime.datetime`
        Starting date for calculating the range of days.

    date_range: str
        Range specifier for size of range to calculate.

    Returns
    -------
    int:
        Number of days within the specified range.
    """
    # TODO: Determine all values needed to be supported and how to calculate multi-month values
    range_map = {
        "1d": 1,
        "1m": monthrange(start.year, start.month)[1],
        "3m": 90,
        "1y": 365
    }

    if date_range in range_map:
        return range_map[date_range]

    raise KeyError(f'Unable to determine range for "{date_range}"')
