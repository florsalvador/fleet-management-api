"""..."""
import pytest
from app import get_taxis

@pytest.fixture()
def app():
    """..."""
    _app = get_taxis()
    _app.config.update({
        "TESTING": True,
    })
    yield _app

@pytest.fixture()
def client(app):
    """..."""
    return app.test_client()
