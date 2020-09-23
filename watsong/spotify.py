"""
This file is a starter for whatever Spotify stuff needs to happen
"""
from typing import List, Optional, Dict
from .structures import Album, Song, Result, AlbumDescription, Feel

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

# TODO: We need to discuss how we want to get this Feel object (can't be a filter param)
mock_feel = Feel(0.5, 0, 0.75, 0)


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
            [
                Song(title=item["name"], uri=item["uri"], features={})
                for item in tracks["items"]
            ],
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


def add_audio_features(songs: List[Song]) -> None:
    song_links = []
    for song in songs:
        song_links.append(song["uri"])

    feature_list = sp.audio_features(song_links)

    for feature in feature_list:
        song_index = feature_list.index(feature)
        feel = {
            "energy": feature["energy"],
            "dance": feature["danceability"],
            "lyrics": feature["speechiness"],
            "valence": feature["valence"],
        }

        song = songs[song_index]
        song["features"] = feel

    return


def filter_songs(song: Song) -> bool:
    hasEnergy = False
    hasDanceability = False
    hasLyrics = False
    hasMelody = False

    if song["features"]["energy"] >= mock_feel.energy:
        hasEnergy = True

    if song["features"]["dance"] >= mock_feel.dance:
        hasDanceability = True

    if song["features"]["lyrics"] >= mock_feel.lyrics:
        hasLyrics = True

    if song["features"]["valence"] >= mock_feel.valence:
        hasMelody = True

    return hasEnergy and hasDanceability and hasLyrics and hasMelody


def printSongs(songs: List[Song]) -> None:
    for song in songs:
        print(song)
        print()

    return


if __name__ == "__main__":
    print("Running Spotify.py")
