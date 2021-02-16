import datetime as dt
import logging
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sdas.constants import UtilityConstants
from sdas.handlers import batch_handler


# TODO: This currently is limited to only retrieving a single data point.
# However, the original prototype was able to accomplish this by using a
# different endpoint (or rather appending '/date/{date}?chartByDay=true')
# We have the issue of needing to be able to build the URI before we call
# this. Tracker: #145
def news_handler(uri: str, options: list, api_key: str) -> list:
    """
    IEX API call with batch support for news data

    This function provides additional pre-processing for news data. Some of
    the pre-processing available includes converting source datetime into
    a valid date string and removes stopwords from the summary text.

    Parameters
    ----------
    uri : str
        Endpoint URI to send request to.
    options : list
        Additional batch options (e.g. range).
    api_key : str
        IEX API token for authorized calls.

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

    logging.info('Fetching raw data')
    raw_data = batch_handler(uri, options, api_key)
    for value in raw_data:
        logging.info('Preprocessing raw data')
        # Preprocess date into the standardized form YYYY-MM-DD
        date = value['date']
        value['date'] = _preprocess_datetime(date)

        # Proprocess summary to remove stopwords
        summary = value['summary']
        value['summary'] = _preprocess_text(summary)

    logging.info('Returning preprocessed data')
    return raw_data


def _preprocess_datetime(timestamp: int) -> str:
    date = dt.datetime.fromtimestamp(timestamp / 1000)
    return date.strftime('%Y-%m-%d')


def _preprocess_text(text: str):
    _nltk_require('tokenizers', 'punkt')
    _nltk_require('corpora', 'stopwords')

    translate_table = dict((ord(char), None) for char in string.punctuation)
    text_tokens = word_tokenize(text.translate(translate_table))

    no_sw = [word for word in text_tokens if not word in stopwords.words()]
    return (" ").join(no_sw)


def _nltk_require(path: str, package: str):
    try:
        nltk.data.find('/'.join([path, package]))
    except LookupError:
        nltk.download(package)
