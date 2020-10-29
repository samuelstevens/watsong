"""
This is the main controller (called blueprints in Flask) for the application.
"""

import random
from typing import Any, List

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    render_template,
    request,
    session,
)

from . import spotify, watson
from .structures import Feel, Song, assert_feel, default_feel

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
                flash(str(err))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            if not current_app.testing:
                spotify.cache(album_descs, current_app.spotify)

            songs = spotify.get_songs(album_descs, current_app.spotify)

            random.shuffle(songs)
            songs = spotify.add_audio_features(songs, current_app.spotify)

            session["songs"] = songs

            if "feel" not in session:
                session["feel"] = default_feel()

            songs = spotify.filter_songs(session["feel"], session["songs"])

    return render_template("jukebox.html", songs=songs, dials=DIALS)


@bp.route("/filter", methods=["GET"])
def filter() -> Any:
    """
    Take a request and its songs and filter them according to DIALS
    """
    feel = Feel(
        valence=request.args.get("valence", 1.0, type=float),
        lyrics=request.args.get("lyrics", 1.0, type=float),
        dance=request.args.get("dance", 1.0, type=float),
        energy=request.args.get("energy", 1.0, type=float),
    )

    session["feel"] = feel

    assert_feel(feel)

    songs = spotify.filter_songs(session["feel"], session["songs"])

    return jsonify(songs)


@bp.route("/showPlaylist", methods=["GET"])
def showPlaylist() -> Any:
    """
    Show embedded spotify playlist
    """
    """url = spotify.create_playlist(session["songs"])"""

    songs = spotify.filter_songs(session["feel"], session["songs"])

    url = spotify.create_playlist(songs, current_app.spotify, full_url=False)
    return jsonify(url)


@bp.route("/subscribe", methods=["GET"])
def subscribe() -> Any:
    try:
        result = {"msg": ""}

        playlist_id = request.args.get("playlistId", type=str)
        if not playlist_id:
            result["msg"] = "No playlist id provided."
            return jsonify(result)
        spotify.subscribe_to_playlist(playlist_id, current_app.spotify)
        result["msg"] = "Subscribed to playlist!"
        return jsonify(result)
    except Exception as e:
        result["msg"] = str(e)
        return jsonify(result)
