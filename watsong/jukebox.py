"""
This is the main controller (called blueprints in Flask) for the application.
"""

import random
from typing import Any, List, cast

from flask import Blueprint, flash, jsonify, render_template, request, session

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
            spotify.cache(album_descs)

            songs, err = spotify.get_songs(album_descs)
            if err is not None:
                flash(str(err))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

            random.shuffle(songs)
            songs, err = spotify.add_audio_features(songs)
            if err is not None:
                flash(str(err))
                return render_template("jukebox.html", songs=songs, dials=DIALS)

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


@bp.route("/showPlaylist",methods=["GET"])
def showPlaylist() -> Any:
    """
    Show embedded spotify playlist
    """
    url = spotify.create_playlist(session["songs"])
    print(url)
    return jsonify(url)


@bp.route("/playlist", methods=["GET"])
def playlist() -> Any:
    """
    Take a request and its songs and filter them according to DIALS
    """

    feel = Feel(
        valence=request.args.get("valence", 1.0, type=float),
        lyrics=request.args.get("lyrics", 1.0, type=float),
        dance=request.args.get("dance", 1.0, type=float),
        energy=request.args.get("energy", 1.0, type=float),
    )

    assert_feel(feel)

    songs = spotify.filter_songs(session["feel"], session["songs"])

    url = spotify.create_playlist(songs)

    return jsonify(url)
