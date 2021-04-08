"""
Provides object validation against a standard schema for pyDAS configuration.
"""

from .exceptions import ValidationError
from .field import Field
from .fieldgroup import FieldGroup

SCHEMA = {
    'testing': Field(bool),
    'database': FieldGroup({
        'dialect': Field(str),
        'hostname': Field(str),
        'port': Field(int),
        'initial_catalog': Field(str),
        'username': Field(str, False)
    }),
    'alembic': FieldGroup({
        'script_location': Field(str),
        'output_encoding': Field(str, False)
    }, False),
    'authentication': FieldGroup({
        'auth_provider': Field(str)
    }, False),
    'logging': FieldGroup({
        'version': Field(int),
        'root': FieldGroup({
            'level': Field(str),
            'handlers': Field(list)
        }),
        'handlers': Field(dict),
        'formatters': Field(dict)
    })
}


def validate_schema(obj, should_raise=False) -> bool:
    """Validates an object against the pyDAS schema and returns a flag indicating whether it passed

    Parameters
    ----------
    obj: any
        The object to be validated

    should_raise: bool
        Flag indicating whether an exception should be raised if validation should fail. Defaults
        to False.

    Raises
    ------
    TypeError:
        Raised if the object is not subscriptable.

    ValidationError:
        Raised if schema validation fails and should_raise is True.
    """
    if not hasattr(obj, '__getitem__'):
        raise TypeError('unsubscriptable object')

    try:
        __validate_schema(SCHEMA, obj)
        return True
    except ValidationError as err:
        if should_raise:
            raise err

        return False


def __validate_schema(schema: dict, obj: dict):
    for key, value in schema.items():
        if key not in obj:
            if value.is_required:
                # Case: key is missing
                raise ValidationError(
                    f"Missing required field or group: '{key}'")
            else:
                continue

        if isinstance(value, FieldGroup):
            # Case: schema value is dict
            __validate_schema(value.fields, obj[key])
        elif not isinstance(obj[key], value.data_type):
            # Case: obj[key] is value.data_type
            raise ValidationError(
                f"Data type does not match for field: {key}")
