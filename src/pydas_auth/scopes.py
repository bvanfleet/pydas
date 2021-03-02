'''
pyDAS API authentication scopes for access various resources via the REST API.
'''

from functools import wraps

# TODO: Determine what the best option may be for removing this coupling with Flask. As it is the
# only coupling with Flask in this package, and removing it may improve maintainability with the
# project as a whole.
from flask import jsonify

from pydas_auth.clients import AuthClientFactory


ACQUIRE_READ = 'pydas-acquire-read'
ARCHIVES_READ = 'pydas-archives-read'
ARCHIVES_WRITE = 'pydas-archives-write'
COMPANIES_READ = 'pydas-companies-read'
COMPANIES_WRITE = 'pydas-companies-write'
COMPANIES_DELETE = 'pydas-companies-delete'
CONFIGURATION_READ = 'pydas-configuration-read'
CONFIGURATION_WRITE = 'pydas-configuration-write'
FEATURES_READ = 'pydas-features-read'
FEATURES_WRITE = 'pydas-features-write'
FEATURES_DELETE = 'pydas-features-delete'
HANDLERS_READ = 'pydas-handlers-read'
OPTIONS_READ = 'pydas-options-read'
OPTIONS_WRITE = 'pydas-options-write'
STATISTICS_READ = 'pydas-statistics-read'


def verify_scopes(scopes, app, request):
    def check_access(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if app.container.config.testing():
                return fn(*args, **kwargs)

            auth_client = AuthClientFactory.get_auth_client(
                app.container.config.authentication.auth_provider(),
                app.container.config.authentication.credentials())
            try:
                token = request.headers.get('Authorization').split()[1]
                uid = auth_client.validate_token(token)
            except Exception as exc:
                return jsonify(msg='Bad authorization header'), 401

            roles = auth_client.get_roles(uid)
            if scopes[request.method] not in roles:
                return jsonify(msg='Unauthorized access'), 403

            return fn(*args, **kwargs)
        return wrapper
    return check_access
