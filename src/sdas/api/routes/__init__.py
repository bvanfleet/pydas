'''Collection of REST API blueprints that can be registered to provide sDAS functionality'''

from .acquire import acquire_bp
from .archives import archives_bp
from .company import company_bp
from .configuration import configuration_bp
from .feature import feature_bp
from .handler import handler_bp
from .option import option_bp
from .statistics import statistics_bp
from .swagger import swaggerui_bp
