from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:5000/api/docs/dist/swagger'

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
