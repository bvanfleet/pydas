"""
IEX Cloud API handler functions that control how data is requested from the REST API.
"""
import datetime as dt
import logging
import requests

from pydas.constants import SdasConstants, UtilityConstants
from pydas.transformers.utils import build_query, calc_range


def batch_handler(uri: str, options: list, api_key: str) -> list:
    """IEX API call with batch support

    Depending on the endpoint, batch operation support is available. This means
    that range operations allow data retrievals to take place in a single call.

    Parameters
    ----------
    uri : str
        Endpoint URI to send request to.
    options : list
        Additional batch options (e.g. range)
    api_key : str
        IEX API token for authorized calls

    Returns
    -------
    list
        Collection of tuples containing the date returned from the API request.

    Raises
    ------
    ValueError
        If either the uri or apiKey are invalid values.
    """
    if uri is None or uri.strip() == UtilityConstants.str_empty:
        raise ValueError('Invalid URI for feature')

    if api_key is None or api_key.strip() == UtilityConstants.str_empty:
        raise ValueError('Invalid API key provided')

    logging.info(
        f'Requesting data from endpoint: "{uri+build_query(options, api_key)}"')
    response = requests.get(uri+build_query(options, api_key))
    response.raise_for_status()
    return response.json()


def tech_indicators_handler(uri: str, options: list, api_key: str) -> list:
    """IEX API call with batch support for technical indicators

    Depending on the endpoint, batch operation support is available. This means
    that range operations allow data retrievals to take place in a single call.
    This function handles additional post-processing required for tech indicators.

    Parameters
    ----------
    uri : str
        Endpoint URI to send request to.
    options : list
        Additional batch options (e.g. range) MUST INCLUDE `feature_name`
    api_key : str
        IEX API token for authorized calls

    Returns
    -------
    list
        Collection of tuples containing the date returned from the API request.

    Raises
    ------
    ValueError
        If either the uri or apiKey are invalid values.
    """
    feature_name = options[0]['feature_name']

    if feature_name == UtilityConstants.str_empty:
        raise KeyError("Feature name was not found in the options collection")

    response = batch_handler(uri, options, api_key)

    chart_len = len(response["chart"])
    indicator_len = len(response["indicator"][0])
    if chart_len != indicator_len:
        logging.warning(
            "Chart and indicator lengths do not match! Using the shortest length, data loss may occur.")

    result = []
    for i in range(indicator_len if indicator_len <= chart_len else chart_len):
        value = response["indicator"][0][i]
        result.append(
            {'date': response["chart"][i]["date"],
             feature_name: value if value is not None else UtilityConstants.str_empty})

    return result


def range_handler(uri: str, options: list, api_key: str) -> list:
    """Calls REST API using options for determining day range for number of values to return

    Parameters
    ----------
    uri : str
        API endpoint to call
    options : list
        Additional endpoint parameters (including start date and range)
    api_key : str
        REST API authentication token

    Returns
    -------
    list:
        Collection of data points returned from REST API

    Raises
    ------
    ValueError:
        If uri or api_key are invalid
    KeyError:
        If given range is not supported
    """
    if uri is None or uri.strip() == UtilityConstants.str_empty:
        raise ValueError('Invalid URI for feature')

    if api_key is None or api_key.strip() == UtilityConstants.str_empty:
        raise ValueError('Invalid API key provided')

    start_date = dt.date.today()
    date_range = '1d'
    for option in options:
        if option[SdasConstants.name_property] == 'exactDate':
            start_date = dt.datetime.strptime(
                option[SdasConstants.value_property],
                '%Y%m%d')

        if option[SdasConstants.name_property] == 'range':
            date_range = option[SdasConstants.value_property]

    range_val = calc_range(start_date, date_range)
    data = []
    for i in range(range_val):
        t_date = start_date - dt.timedelta(days=i)
        # Check if weekday is Saturday or Sunday (5 or 6 respectively) and skip data retrieval
        if t_date.weekday() > 4:
            continue

        query = build_query(
            [{
                'name': 'exactDate',
                'value': t_date.strftime('%Y%m%d')}],
            api_key)
        response = requests.get(uri + query)
        response.raise_for_status()
        point = response.json()
        if SdasConstants.date_property not in point:
            point[SdasConstants.date_property] = t_date.strftime('%Y-%m-%d')

        data.append(point)

    return data
