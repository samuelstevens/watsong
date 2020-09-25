"""
This is the main controller (called blueprints in Flask) for the application.
"""

import random
from typing import Any, List, cast

from flask import Blueprint, jsonify, render_template, request, session

from . import spotify, watson
from .structures import Song, default_feel

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

            spotify.add_audio_features(songs)

            session.clear()
            session["songs"] = songs

            if "feel" not in session:
                session["feel"] = default_feel()

            songs = [
                song
                for song in cast(List[Song], session["songs"])
                if spotify.filter_songs(session["feel"], song)
            ]

    return render_template("jukebox.html", songs=songs, dials=DIALS)


@bp.route("/filter", methods=["GET"])
def filter() -> Any:
    """
    Take a request and its songs and filter them according to DIALS
    """

    field: str = request.args["name"]
    level = float(request.args["level"])

    if "feel" not in session:
        session["feel"] = default_feel()

    session["feel"][field] = level

    songs = [
        song
        for song in cast(List[Song], session["songs"])
        if spotify.filter_songs(session["feel"], song)
    ]

    return jsonify(songs)
