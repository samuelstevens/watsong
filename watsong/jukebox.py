"""
This is the main controller (called blueprints in Flask) for the application.
"""

import random
from typing import Any, List, Dict, Union

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

DIALS = ["dance", "lyrics", "energy", "happiness"]


@bp.route("/", methods=["GET", "POST"])
def jukebox() -> Any:
    """
    Renders the empty jukebox page.
    """
    songs: List[Song] = []
    query = ""
    if request.method == "POST":
        query = request.form["query"]

        if query:
            album_descs, err = watson.get_albums(query)
            if len(album_descs) == 0:
                flash(
                    "Your query was not descriptive enough to match to a song well. Try adding more descriptive words."
                )
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            if err is not None:
                flash(str(err))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            if not album_descs:
                flash("Invalid input")
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            if not current_app.testing:
                spotify.cache(album_descs, current_app.spotify)
            try:
                songs = spotify.get_songs(album_descs, current_app.spotify)
            except Exception as e:
                flash(str(e))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            random.shuffle(songs)
            try:
                songs = spotify.add_audio_features(songs, current_app.spotify)
            except Exception as e:
                flash(str(e))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            session["songs"] = songs

            if "feel" not in session:
                session["feel"] = default_feel()

            try:
                songs = spotify.filter_songs(session["feel"], session["songs"])
            except Exception as e:
                flash(str(e))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

    return render_template("jukebox.html", songs=songs, dials=DIALS, query=query)


@bp.route("/filter", methods=["GET"])
def filter() -> Any:
    """
    Take a request and its songs and filter them according to DIALS
    """
    feel = Feel(
        valence=request.args.get("valence", 0.5, type=float),
        lyrics=request.args.get("lyrics", 0.5, type=float),
        dance=request.args.get("dance", 0.5, type=float),
        energy=request.args.get("energy", 0.5, type=float),
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
    songs = spotify.filter_songs(session["feel"], session["songs"])

    url = spotify.create_playlist(songs, current_app.spotify, full_url=False)
    return jsonify(url)


@bp.route("/subscribe", methods=["GET"])
def subscribe() -> Any:
    result = {"msg": ""}
    try:
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


@bp.route("/logout", methods=["GET"])
def logout() -> Any:
    result: Dict[str, Union[str, bool]] = {}
    try:
        result_str = spotify.logout()
        result["success"] = result_str == ""
        if not result["success"]:
            result["msg"] = result_str
    except Exception as e:
        result["success"] = False
        result["msg"] = str(e)
    return jsonify(result)
