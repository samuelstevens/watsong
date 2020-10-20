"""
This file is a starter for whatever Spotify stuff needs to happen
"""
import pickle
from typing import Any, Dict, List, Optional

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

import util
from structures import Album, AlbumDescription, Feel, Result, Song

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

# Client credentials for spotify. May be a bit faster to run.
spcc = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
)


def query(title: str, artists: List[str]) -> str:
    return f"{title}"


def get_memo(name: str) -> Any:
    try:
        with open(f"{name}.pickle", "rb") as file:
            return pickle.load(file)
    except IOError:
        return {}


def set_memo(structure: Any, name: str) -> None:
    try:
        with open(f"{name}.pickle", "wb") as file:
            pickle.dump(structure, file, protocol=4)
    except IOError:
        print(f"Error with saving {name}.pickle when trying to save {structure}")


search_memo = get_memo("search")
album_tracks_memo = get_memo("tracks")
feature_memo = get_memo("features")


def cache(album_descriptions: List[AlbumDescription]) -> None:
    """
    Cache the results for the given album descriptions for fast lookup later.
    Calling this before using the spotify methods on a list of albums will improve
    performance.
    """
    global search_memo
    global album_tracks_memo
    global feature_memo
    missed = [False, False, False]
    for title, artists in album_descriptions:
        q = query(title, artists)
        try:
            search_result = search_memo[q]
        except KeyError:
            missed[0] = True
            search_result = spcc.search(query(title, artists), type="album", limit=50)
            search_memo[q] = search_result
        album_id = find_album_id_from_search(search_result, artists)
        if album_id:
            try:
                album_tracks_memo[album_id] = album_tracks_memo[album_id]
            except KeyError:
                missed[1] = True
                album_tracks_memo[album_id] = spcc.album_tracks(album_id)
    if missed[0]:
        set_memo(search_memo, "search")
    if missed[1]:
        set_memo(album_tracks_memo, "tracks")

    songs, err = get_songs(album_descriptions)
    for songs_chunk in util.chunks(iter(songs), 100):
        seenAllSongs = True
        song_links = [song["uri"] for song in songs_chunk]
        for link in song_links:
            if link not in feature_memo:
                seenAllSongs = False
        if not seenAllSongs:
            missed[2] = True
            feature_list = spcc.audio_features(song_links)
            for uri, features in zip(song_links, feature_list):
                feature_memo[uri] = features

    if missed[2]:
        set_memo(feature_memo, "features")


def find_album_id_from_search(
    search: Dict[str, Any], artists: List[str]
) -> Optional[str]:
    results = search["albums"]["items"]

    album_id = None
    if len(results) > 0:
        # Go through results and find the album with the desired artist
        for result in results:
            artist = result["artists"][0]["name"]
            if artist in artists:
                album_id = result["id"]
                break

        if album_id is None:
            album_id = results[0]["id"]
    return album_id


def album_from_title_artist(title: str, artists: List[str]) -> Optional[Album]:
    """
    Return an album
    :return:
    """
    q = query(title, artists)
    try:
        search_result = search_memo[q]
    except KeyError:
        search_result = spcc.search(q, type="album", limit=50)
        print(f"Key error looking up the query {q}")
    album_id = find_album_id_from_search(search_result, artists)
    if album_id:
        try:
            tracks = album_tracks_memo[album_id]
        except KeyError:
            tracks = spcc.album_tracks(album_id)
            print(f"Key error looking up the track with id {album_id}")
        return Album(
            title,
            album_id,
            artists,
            [
                Song(
                    title=item["name"],
                    uri=item["uri"],
                    features={},
                    artists=[artist["name"] for artist in item["artists"]],
                )
                for item in tracks["items"]
            ],
        )

    return None


def get_songs(album_descriptions: List[AlbumDescription]) -> Result[List[Song]]:
    """
    Given a list of albums, find all the songs in those albums according to Spotify.
    """
    songs = []
    for title, artistList in album_descriptions:
        result = album_from_title_artist(title, artistList)

        if not result:
            continue

        title, id, artists, tracks = result
        songs.extend(tracks)

    return songs, None


def add_audio_features(songs: List[Song]) -> Result[List[Song]]:
    if not songs:
        return [], None

    annotated_songs = []
    feature_list = []
    for song in songs:
        try:
            features = feature_memo[song["uri"]]
        except KeyError:
            features = spcc.audio_features(song["uri"])[0]
        feature_list.append(features)

    for song, features in zip(songs, feature_list):
        feel = {
            "energy": features["energy"],
            "dance": features["danceability"],
            "lyrics": features["speechiness"],
            "valence": features["valence"],
        }

        song["features"] = feel
        annotated_songs.append(song)

    return annotated_songs, None


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
    sp.playlist_replace_items(playlist["id"], [song["uri"] for song in songs[:100]])
    return f'https://open.spotify.com/embed/playlist/{playlist["id"]}'
    

"""Given a list of playlist/album ids find the net average 
feature data (acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo)
for the entire collection of songs in the playlists/albums"""

def get_album_features(ids: List[str]) -> Dict[str, float]:
    all_features = {
        "danceability": [],
        "energy": [],
        "key": [],
        "loudness": [],
        "mode": [],
        "speechiness": [],
        "acousticness": [],
        "instrumentalness": [],
        "liveness": [],
        "valence": [],
        "tempo": []
    }

    for id in ids:
        songsPerTrack = sp.album_tracks(id)['items']

        for song in songsPerTrack:
            featuresForSong = sp.audio_features(song['uri'])

            for feature_type in featuresForSong[0].keys():
                if feature_type in all_features.keys():
                    value_of_feature = featuresForSong[0][feature_type]
                    all_features[feature_type].append(value_of_feature)

    for (feature_name, values) in all_features.items():
        all_features[feature_name] = sum(values) / len(values)

    return all_features

def get_playlist_features(ids: List[str]) -> Dict[str, float]:
    all_features = {
        "danceability": [],
        "energy": [],
        "key": [],
        "loudness": [],
        "mode": [],
        "speechiness": [],
        "acousticness": [],
        "instrumentalness": [],
        "liveness": [],
        "valence": [],
        "tempo": []
    }

    for id in ids:
        songsPerTrack = sp.playlist_tracks(id)['items']

        for song in songsPerTrack:
            featuresForSong = sp.audio_features(song['track']['uri'])

            for feature_type in featuresForSong[0].keys():
                if feature_type in all_features.keys():
                    value_of_feature = featuresForSong[0][feature_type]
                    all_features[feature_type].append(value_of_feature)

    for (feature_name, values) in all_features.items():
        all_features[feature_name] = sum(values) / len(values)

    return all_features

"""Return count album ids which are the most popular and relevant to the input query"""
def get_album_ids(query: str, count: int) -> List[str]:
    result = sp.search(query, count, type="album")

    ids = []
    for playlist in result['albums']['items']:
        ids.append(playlist['id'])

    return ids

"""Return count playlist ids which are the most popular and relevant to the input query"""
# Note @param count can be max 50
def get_playlist_ids(query: str, count: int) -> List[str]:
    result = sp.search(query, count, type="playlist")

    ids = []
    for playlist in result['playlists']['items']:
        ids.append(playlist['id'])

    return ids

def average_of_album_playlist_features(album_features: dict, playlist_features: dict):
    average_features = {
        "danceability": None,
        "energy": None,
        "key": None,
        "loudness": None,
        "mode": None,
        "speechiness": None,
        "acousticness": None,
        "instrumentalness": None,
        "liveness": None,
        "valence": None,
        "tempo": None
    }

    if len(set(album_features.keys()).difference(set(playlist_features.keys()))) == 0:
        feature_types = album_features.keys()

        for feature_name in feature_types:
            average_features[feature_name] = (album_features[feature_name] + playlist_features[feature_name]) / 2

    return average_features




        

    


