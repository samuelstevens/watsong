"""
This file is a starter for whatever Spotify stuff needs to happen
"""
from typing import List
from .structures import Album, Song, Result
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Authenticate with spotify using the client credientials flow.
# We can then access the spotify API, so long as we don't need
# access to user information.
# :return:
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="5d141ce6f09c4fbfa12d16ce9e5d40c1",
                                                           client_secret="52fed0d6564a4e6f8e596b78bd1abf62"))


def album_from_title_artist(title: str, artists: List[str]) -> Album:
    """
    Return an album
    :return:
    """
    # TODO Nothing is returned when I also search for artist
    search_result = sp.search(f"album:{title}", type="album", limit=1)
    results = search_result["albums"]["items"]
    if len(results) > 0:
        album_id = results[0]["id"]
        tracks = sp.album_tracks(album_id)
        return title, album_id, artists, tracks
    return title, None, artists, None


def get_songs(albumDesc: List) -> Result[List[Song]]:
    """
    Given a list of albums, find all the songs in those albums according to Spotify.
    """
    songs = []
    for [title, artist] in albumDesc:
        title, id, artists, tracks = album_from_title_artist(title, artist)
        for song in tracks["items"]:
            # You can get more stuff like the song id if you want to...
            # https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/
            songs.append({"title": song["name"]})
    return songs, None


album_list = [("A girl between two worlds", ["Fatima Yamaha"]), ("Harder", ["Jax Jones, Bebe Rexha"])]
songs, errors = get_songs(album_list)
print(songs)
