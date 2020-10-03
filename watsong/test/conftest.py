# type: ignore

import pytest
from typing import Any
from .. import webapp
import flask


@pytest.fixture()
def app() -> Any:
    """
    Create and configure a new app instance for each test
    """

    app = webapp.create_app({"TESTING": True})

    yield app


@pytest.fixture()
def client(app: flask.Flask) -> Any:
    return app.test_client()