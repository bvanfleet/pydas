from .builder import build_config
from .schema import validate_schema, ValidationError
from .section import ConfigSection

# TODO: Need to create a config object that provides more operations and integrates the
# ConfigSection class better. It may be best to create this in a separate module so it
# can be picked up by the build_config function.

__version__ = '0.1.0'
