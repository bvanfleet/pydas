from pydas import app


def app_client():
    app.config["TESTING"] = True
    app.config["DB_DIALECT"] = 'mock'
    return app.test_client()
