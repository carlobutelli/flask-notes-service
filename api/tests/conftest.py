import os

import pytest

from .. import create_app


@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    os.environ['FLASK_ENV'] = "Testing"
    app = create_app()

    ctx = app.app_context()
    ctx.push()

    client = app.test_client()

    yield client
