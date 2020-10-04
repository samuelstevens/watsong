# type: ignore

import flask

from .. import spotify, structures


def test_index(client):
    response = client.get("/")
    assert b"redirect" in response.data
    assert b"jukebox" in response.data


def test_jukebox(client):
    response = client.get("/jukebox/")
    assert b"redirect" not in response.data
    assert b"Watsong" in response.data


def test_query_frontend(client):
    response = client.post(
        "/jukebox/",
        data=dict(query="Beach songs"),
        follow_redirects=True,
    )
    assert b"Kevin Gates" in response.data
    assert b"redirect" not in response.data
    assert b"Watsong" in response.data


def test_query_form(app):
    with app.test_request_context(
        "/jukebox/", method="POST", data=dict(query="Beach songs")
    ):
        assert flask.request.method == "POST"
        assert flask.request.path == "/jukebox/"
        assert "query" in flask.request.form
        assert flask.request.form["query"] == "Beach songs"


def test_query_session_feel(app):
    with app.test_client() as c:
        c.post(
            "/jukebox/",
            data=dict(query="Beach songs"),
            follow_redirects=True,
        )
        assert "feel" in flask.session
        assert flask.session["feel"] == structures.default_feel()


def test_query_session_songs(app):
    with app.test_client() as c:
        response = c.post(
            "/jukebox/",
            data=dict(query="Beach songs"),
            follow_redirects=True,
        )
        assert "songs" in flask.session

        for song in flask.session["songs"]:
            if spotify.filter_songs(flask.session["feel"], song):
                assert (
                    bytes(flask.escape(song["title"]), encoding="utf8") in response.data
                )


def test_query_filter(app):
    dance_value = 0.1
    valence_value = 0.2
    energy_value = 0.3
    lyrics_value = 0.2

    with app.test_client() as c:
        # initialize the session with a query
        c.post(
            "/jukebox/",
            data=dict(query="Beach songs"),
            follow_redirects=True,
        )
        assert "songs" in flask.session

        response = c.get(
            f"/jukebox/filter?dance={dance_value}&valence={valence_value}&energy={energy_value}&lyrics={lyrics_value}"
        )

        # assert that the session feel has been updated
        assert "feel" in flask.session
        assert flask.session["feel"]["dance"] == dance_value
        assert flask.session["feel"]["valence"] == valence_value
        assert flask.session["feel"]["energy"] == energy_value
        assert flask.session["feel"]["lyrics"] == lyrics_value

        assert "songs" in flask.session

        response_song_titles = set()

        # check that all sent songs make it past the filter
        for song in response.json:
            assert spotify.filter_songs(flask.session["feel"], song)
            response_song_titles.add(song["title"])

        # check that all songs that make it past the filter are actually sent
        for song in flask.session["songs"]:
            if spotify.filter_songs(flask.session["feel"], song):
                assert song["title"] in response_song_titles
