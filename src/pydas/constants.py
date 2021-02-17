'''
sDAS REST API constants used throughout the application
'''

HTTP_DELETE = 'DELETE'
HTTP_GET = 'GET'
HTTP_PATCH = 'PATCH'
HTTP_POST = 'POST'

BASE_PATH = '/'


class SdasConstants:
    """Common sDAS utility strings"""
    date_property = 'date'
    header_property = 'header'
    name_property = 'name'
    value_property = 'value'
    multi_value_property = 'values'


class UtilityConstants:
    """Utility constant values not pre-defined by Python"""
    str_empty = ''


class FeatureToggles:
    event_handlers = 'enable_event_handlers'
