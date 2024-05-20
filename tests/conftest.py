"""..."""
import pytest
from app.app import main

@pytest.fixture()
def app():
    """..."""
    _app = main()
    _app.config.update({
        "TESTING": True,
    })
    yield _app

@pytest.fixture()
def client(app):
    """..."""
    return app.test_client()
