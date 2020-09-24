"""
This is the main controller (called blueprints in Flask) for the application.
"""

import random

from flask import Blueprint, render_template, request, jsonify, session

from . import watson, spotify
from .structures import Song, Feel
from typing import Any, List

bp = Blueprint("jukebox", __name__, url_prefix="/jukebox")

DIALS = ["dance", "lyrics", "energy", "valence"]


@bp.route("/", methods=["GET", "POST"])
def jukebox() -> Any:
    """
    Renders the empty jukebox page.
    """
    songs: List[Song] = []

    if request.method == "POST":
        query = request.form["query"]

        if query:
            album_descs, err = watson.get_albums(query)

            if err is not None:
                return jsonify({"error": str(err)})

            songs, err = spotify.get_songs(album_descs)

            if err is not None:
                return jsonify({"error": str(err)})

            random.shuffle(songs)

            session.clear()
            session["songs"] = songs

    return render_template("jukebox.html", songs=songs, dials=DIALS)


@bp.route("/filter", methods=["GET"])
def filter() -> Any:
    """
    Take a request and its songs and filter them according to DIALS
    """
    print(request.args)
    params = [request.args.get(dial.lower(), 0, type=float) for dial in DIALS]

    print(params)

    # TODO
    # feel = Feel(params)

    # TODO: actually filter using spotify.filter_songs
    session["songs"] = session["songs"]

    return jsonify(session["songs"])
