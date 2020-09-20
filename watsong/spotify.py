"""
This file is a starter for whatever Spotify stuff needs to happen
"""
from typing import List, Optional
from .structures import Album, Song, Result, AlbumDescription

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Authenticate with spotify using the client credientials flow.
# We can then access the spotify API, so long as we don't need
# access to user information.
# :return:
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="5d141ce6f09c4fbfa12d16ce9e5d40c1",
        client_secret="52fed0d6564a4e6f8e596b78bd1abf62",
    )
)


def album_from_title_artist(title: str, artists: List[str]) -> Optional[Album]:
    """
    Return an album
    :return:
    """
    # Set max limit for now...
    search_result = sp.search(f"album:{title}", type="album", limit=50)
    results = search_result["albums"]["items"]

    if len(results) > 0:
        album_id = None

        # Go through results and find the album with the desired artist
        for result in results:
            artist = result["artists"][0]["name"]
            if artist in artists:
                album_id = result["id"]
                break

        if album_id is None:
            album_id = results[0]["id"]

        tracks = sp.album_tracks(album_id)
        return Album(
            title,
            album_id,
            artists,
            # You can get more stuff like the song id if you want to...
            # https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/
            [Song(title=item["name"]) for item in tracks["items"]],
        )

    return None


def get_songs(album_descriptions: List[AlbumDescription]) -> Result[List[Song]]:
    """
    Given a list of albums, find all the songs in those albums according to Spotify.
    """
    songs = []
    for title, artist in album_descriptions:
        result = album_from_title_artist(title, artist)

        if not result:
            continue

        title, id, artists, tracks = result
        songs.extend(tracks)

    return songs, None


# TODO: Create a filter API based on the Feel values
# def filter_songs(songs: List[Song], feel: Feel) -> List[Song]:
#     return


if __name__ == "__main__":
    print("Running Spotify.py")
