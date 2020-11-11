import os
from typing import Any, Optional

from flask import Flask, redirect, url_for

from flask_session import Session

from . import jukebox, spotify
from .test.spotify_mocks import between_worlds_mock

SESSION = Session()


def create_app(test_config: Optional[Any] = None) -> Flask:
    """
    Creates and configures the app. Flask uses this as the entry point.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=os.environ["SECRET_KEY"])

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    app.register_blueprint(jukebox.bp)

    @app.route("/")
    def index() -> Any:
        """
        Redirect index to /jukebox
        """
        return redirect(url_for("jukebox.jukebox"))

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_TYPE="filesystem",
    )

    SESSION.init_app(app)
    app.get_spotify = between_worlds_mock if app.testing else spotify.get_spotify

    return app
