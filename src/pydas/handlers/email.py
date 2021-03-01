from email.message import EmailMessage
from enum import Enum
import logging
import smtplib
import traceback
from typing import List

from dependency_injector.wiring import inject, Provide

from pydas_metadata.contexts import BaseContext
from pydas_metadata.models import Configuration

from pydas.containers import ApplicationContainer


class Notification(Enum):
    """
    Email notification types enumeration.

    Attributes
    ----------
    INFO: 1
        Informational email notification.

    ERROR: 2
        Error email notification.
    """
    INFO = 1
    ERROR = 2


def send_notification(*args, **kwargs):
    notification_type = kwargs['type']
    uri = kwargs['uri']

    if Notification[notification_type] == Notification.ERROR:
        if 'exception' not in kwargs:
            raise KeyError(
                'Unable to send error notification without exception!')

        email_error(uri, kwargs['exception'])

    if Notification[notification_type] == Notification.INFO:
        if 'message' not in kwargs:
            kwargs['message'] = 'No message provided, please contact the system administrator.'

        email_information(uri, kwargs['message'])


def email_information(uri: str, message: str):
    smtp_config = get_smtp_config()
    email = EmailMessage()
    email.set_content(
        f'''sDAS Notification for operation

        Operation URI: {uri}

        {message}
        ''')
    email['Subject'] = 'sDAS System Notification'
    email['From'] = smtp_config['fromAddress']
    email['To'] = smtp_config['toAddress']

    logging.debug("Sending email message to %s", smtp_config['To'])
    with smtplib.SMTP_SSL(smtp_config['hostname'], port=smtp_config['port']) as smtp:
        smtp.login(smtp_config['username'], smtp_config['password'])
        smtp.send_message(email)
        smtp.quit()

    logging.debug("Email message sent!")


def email_error(uri: str, exception: Exception):
    smtp_config = get_smtp_config()

    if exception is not None:
        exception_trace = ('').join(
            traceback.format_tb(exception.__traceback__))
    else:
        exception_trace = 'Invalid exception object provided'

    email = EmailMessage()
    email.set_content(
        f'''Unable to complete operation!

        Operation URI: {uri}

        Error Message: {exception}
        Error Type: {exception.__class__.__name__}
        Stack Trace: {exception_trace}
        ''')
    email['Subject'] = 'sDAS System Error Notification'
    email['From'] = smtp_config['fromAddress']
    email['To'] = smtp_config['toAddress']

    logging.debug("Sending email message to %s", email['To'])
    with smtplib.SMTP_SSL(smtp_config['hostname'], port=smtp_config['port']) as smtp:
        smtp.login(smtp_config['username'], smtp_config['password'])
        smtp.send_message(email)
        smtp.quit()

    logging.debug("Email message sent!")

# TODO: Need to hook up some dynamic dependency injection in order for this to work.


@inject
def get_smtp_config(
        metadata_context: BaseContext = Provide[ApplicationContainer.context_factory]) -> dict:
    """
    Retrieves the SMTP configuration from the metadata store.

    Returns
    -------
    dict:
        Dictionary object containing retrieved SMTP settings.

    Raises
    ------
    TypeError:
        Thrown if the configuration object cannot be mapped to a known SMTP configuration.
    """
    logging.debug("Fetching all SMTP configuration from sDAS database")
    session = metadata_context.get_session()
    smtp_configs: List[Configuration] = session.query(Configuration).filter(
        Configuration.name.ilike('smtp%')).all()

    config = {
        'fromAddress': '',
        'toAddress': '',
        'hostname': '',
        'port': 465,
        'username': '',
        'password': ''
    }

    for smtp_config in smtp_configs:
        # Here's how we hack a switch statement in Python :)
        if smtp_config.name == 'smtpFromAddress':
            config['fromAddress'] = smtp_config.value
        elif smtp_config.name == 'smtpToAddress':
            config['toAddress'] = smtp_config.value
        elif smtp_config.name == 'smtpHostname':
            config['hostname'] = smtp_config.value
        elif smtp_config.name == 'smtpPort':
            config['port'] = int(smtp_config.value)
        elif smtp_config.name == 'smtpUsername':
            config['username'] = smtp_config.value
        elif smtp_config.name == 'smtpPassword':
            config['password'] = smtp_config.value
        else:
            raise TypeError(
                f'Unknown SMTP configuration value encountered ("{smtp_config.name}")')

    return config
