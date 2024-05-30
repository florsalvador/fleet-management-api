"""Module conftest"""

import pytest
from api.app import main


@pytest.fixture()
def app():
    """Fixture for app"""
    _app = main()
    _app.config.update({
        "TESTING": True,
    })
    with _app.app_context():
        yield _app


# pylint: disable=redefined-outer-name
@pytest.fixture()
def client(app):
    """Fixture for client"""
    return app.test_client()
