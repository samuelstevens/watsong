"""
This is the main controller (called blueprints in Flask) for the application.
"""

from flask import Blueprint, render_template, request, flash, jsonify

from . import watson, spotify

bp = Blueprint("jukebox", __name__, url_prefix="/jukebox")


@bp.route("/", methods=["GET"])
def jukebox():
    return render_template("jukebox.html")


@bp.route("/_nat_lang_query", methods=["GET"])
def nat_lang_query():
    query = request.args.get("query", "", type=str)

    albums, err = watson.get_albums(query)

    if err is not None:
        return jsonify({"error": str(err)})

    songs, err = spotify.get_songs(albums)

    if err is not None:
        return jsonify({"error": str(err)})

    return jsonify(songs)
