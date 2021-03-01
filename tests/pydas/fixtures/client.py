from pydas import create_app

TEST_CONFIG = {
    "testing": True,
    "database": {
        "dialect": "mock"
    }
}


def app_client():
    app = create_app()
    app.container.config.from_dict(TEST_CONFIG)
    return app.test_client()
