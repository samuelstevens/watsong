"""
This is the main controller (called blueprints in Flask) for the application.
"""

from flask import Blueprint, render_template, request, jsonify, session

from . import watson, spotify

bp = Blueprint("jukebox", __name__, url_prefix="/jukebox")

DIALS = ["energy", "lyrics", "dance", "melody"]


@bp.route("/", methods=["GET", "POST"])
def jukebox():
    """
    Renders the empty jukebox page.
    """
    songs = []

    if request.method == "POST":
        query = request.form["query"]

        print(query)

        if query:
            albums, err = watson.get_albums(query)

            if err is not None:
                return jsonify({"error": str(err)})

            songs, err = spotify.get_songs(albums)

            if err is not None:
                return jsonify({"error": str(err)})

            session.clear()
            session["songs"] = songs

    return render_template("jukebox.html", songs=songs, dials=DIALS)
