import logging
from typing import Callable
from sdas.constants import SdasConstants, UtilityConstants


class Feature():
    '''
    *DEPRECATED*: This class should no longer be used. Instead, use the metadata.models.feature API.
    '''

    def __init__(self,
                 name: str,
                 uri: str,
                 handler: Callable[[str, list, str], list],
                 options: list):
        logging.warn(
            '''DEPRECATED: The Feature class is no longer maintained and should not be used!
            We recommend the use of the metadata.models API for interacting with features.
            The sdas.feature_mapper module will be removed in a future date.
            ''')
        self.name = name
        self.uri = uri
        self.handler = handler
        self.options = options

    def __str__(self):
        return f'{{name: {self.name}, uri: {self.uri}, options: {self.options} }}'

    def get_value(self, data: dict):
        if self.name in data:
            return (data[self.name], data[SdasConstants.date_property])
        else:
            return UtilityConstants.str_empty

    def get_values(self, data: list) -> list:
        return [self.get_value(d) for d in data]
