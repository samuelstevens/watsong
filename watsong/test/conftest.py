# type: ignore

from typing import Any

import flask
import pytest

from .. import webapp


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
