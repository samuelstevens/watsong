import functools

from flask import Blueprint, render_template, request, flash, jsonify

from . import watson, spotify

bp = Blueprint("jukebox", __name__, url_prefix="/jukebox")


@bp.route("/", methods=["GET"])
def jukebox():
    return render_template("jukebox.html")


@bp.route("/_nat_lang_query", methods=["GET"])
def nat_lang_query():
    query = request.args.get("query", "", type=str)

    # do some processing here with Watson
    print("query for Watson:", query)

    albums, err = watson.get_albums(query)

    if err is not None:
        return jsonify({"error": str(err)})

    songs, err = spotify.get_songs(albums)

    if err is not None:
        return jsonify({"error": str(err)})

    songs = [
        {
            "song": "Under the Boardwalk",
            "album": "Under the Boardwalk",
            "artist": "The Drifters",
        },
        {
            "song": "What's Love Got to Do with It",
            "album": "Private Dancer",
            "artist": "Tina Turner",
        },
        {
            "song": "This Is The Life",
            "album": "This Is The Life",
            "artist": "Amy Macdonald",
        },
        {
            "song": "I'll Wait",
            "album": "Golden Hour",
            "artist": "Sasha Sloan, Kygo",
        },
    ]

    return jsonify(songs)
