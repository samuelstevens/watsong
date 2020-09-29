"""
This file is a starter for whatever Spotify stuff needs to happen
"""
from typing import List, Optional

import spotipy
from requests import HTTPError
from spotipy.oauth2 import SpotifyOAuth

from . import util
from .structures import Album, AlbumDescription, Feel, Result, Song

# These are also stored in the environment but it's easier to leave them here
# since it causes some problems in how I run it if I use the envionment variables
CLIENT_ID = "5d141ce6f09c4fbfa12d16ce9e5d40c1"
CLIENT_SECRET = "52fed0d6564a4e6f8e596b78bd1abf62"
USERNAME = "mo8wax9tenoczvhquxllzca37"

# If it doesn't work, try deleting the .cache file... will look for a more consistent solution
# later. Actually it tends to work and just give an error message so it's not that bad.
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:8888/callback",
        scope="playlist-modify-public playlist-modify-private",
    )
)


def album_from_title_artist(title: str, artists: List[str]) -> Optional[Album]:
    """
    Return an album
    :return:
    """
    # Set max limit for now...
    search_result = sp.search(f"{title}", type="album", limit=50)
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
                Song(title=item["name"], uri=item["uri"], features={}, artist=artist)
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


def add_audio_features(songs: List[Song]) -> Result[List[Song]]:
    if not songs:
        return [], None

    annotated_songs = []

    for songs_chunk in util.chunks(iter(songs), 20):
        song_links = []
        for song in songs_chunk:
            song_links.append(song["uri"])

        try:
            feature_list = sp.audio_features(song_links)
        except HTTPError as err:
            return [], err

        for song, features in zip(songs_chunk, feature_list):
            feel = {
                "energy": features["energy"],
                "dance": features["danceability"],
                "lyrics": features["speechiness"],
                "valence": features["valence"],
            }

            song["features"] = feel
            annotated_songs.append(song)

    return annotated_songs, None


# TODO: Create a filter API based on the Feel values
def filter_songs(feel: Feel, song: Song) -> bool:
    hasEnergy = False
    hasDanceability = False
    hasLyrics = False
    hasValence = False
    if song["features"]["energy"] >= feel["energy"]:
        hasEnergy = True

    if song["features"]["dance"] >= feel["dance"]:
        hasDanceability = True

    if song["features"]["lyrics"] >= feel["lyrics"]:
        hasLyrics = True

    if song["features"]["valence"] >= feel["valence"]:
        hasValence = True

    return hasEnergy and hasDanceability and hasLyrics and hasValence


def create_playlist(songs: List[Song]) -> str:
    # Find the watsong playlist and use it if possible
    playlists = sp.current_user_playlists()
    watsong_list = [
        playlist
        for playlist in playlists["items"]
        if playlist["name"] == "Watsong Playlist"
    ]
    if len(watsong_list):
        # Get the first playlist named 'Watsong Playlist'
        playlist = watsong_list[0]
        # Clear it
    else:
        # If we can't find it, create a new one.
        playlist = sp.user_playlist_create(
            USERNAME,
            "Watsong Playlist",
            public=True,
            collaborative=True,
            description="A playlist created by watsong just for you",
        )
    sp.playlist_replace_items(playlist["id"], [song["uri"] for song in songs])
    return f'https://open.spotify.com/embed/playlist/{playlist["id"]}'


def print_songs(songs: List[Song]) -> None:
    for song in songs:
        print(song)
        print()
    return


if __name__ == "__main__":
    album_list = [
        AlbumDescription("A girl between worlds", []),
    ]
    songs, errors = get_songs(album_list)
    x = create_playlist(songs)
    print(x)
