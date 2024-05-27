"""..."""
import pytest
from api.app import main

@pytest.fixture()
def app():
    """..."""
    _app = main()
    _app.config.update({
        "TESTING": True,
    })
    with _app.app_context():
        yield _app

@pytest.fixture()
def client(app):
    """..."""
    return app.test_client()
