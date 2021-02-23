from pydas import create_app


def app_client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["DB_DIALECT"] = 'mock'
    return app.test_client()
