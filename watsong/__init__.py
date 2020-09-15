import os

from flask import Flask, redirect, url_for

from . import jukebox

from typing import Optional, Any


def create_app(test_config: Optional[Any] = None) -> Flask:
    """
    Creates and configures the app. Flask uses this as the entry point.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ["SECRET_KEY"],
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

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

    return app