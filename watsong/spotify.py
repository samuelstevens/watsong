"""
A file to communicate with the spotify API
"""
import heapq
import os
import pickle
from typing import Any, Dict, Generic, List, Optional

import flask
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing_extensions import TypedDict

from . import util
from .structures import Album, AlbumDescription, Feel, Song
from .test.spotify_mocks import between_worlds_mock

# These are also stored in the environment but it's easier to leave them here
# since it causes some problems in how I run it if I use the environment variables
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
CACHE_PATH = os.path.join(os.getcwd(), ".cache")

# region types


class SpotifyFeatures(TypedDict):
    energy: float
    danceability: float
    speechiness: float
    valence: float


class SpotifyArtist(TypedDict):
    name: str


class SpotifyTrack(TypedDict):
    name: str
    uri: str
    artists: List[SpotifyArtist]


class SpotifyAlbum(TypedDict):
    artists: List[SpotifyArtist]
    id: str


class HasItems(Generic[util.T]):
    def __getitem__(self, s: str) -> List[util.T]:
        # represents ['items'] returning a list of something. Generic TypedDicts are not supported by MyPy yet.
        ...


class SpotifySearch(TypedDict):
    albums: HasItems[SpotifyAlbum]


# endregion


def get_spotify() -> spotipy.Spotify:
    """
    Creates a spotify client, which will not be logged in until necessary.

    When it's necessary to log in (show playlist), it will open a browser window and wait for the response.

    Sometimes we never get a response
    """
    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            cache_path=CACHE_PATH,
            redirect_uri="http://localhost:7233/callback",
            scope="playlist-modify-public playlist-modify-private",
            show_dialog=True,
        )
    )

    return sp


def init_app(app: flask.Flask) -> flask.Flask:
    if app.testing:
        app.spotify = between_worlds_mock()
    else:
        app.spotify = get_spotify()
    return app


def query(title: str, artists: List[str]) -> str:
    return f"{title}"


def get_memo(name: str) -> Any:
    try:
        with open(f"{name}.pickle", "rb") as file:
            return pickle.load(file)
    except (IOError, EOFError):
        return {}


def set_memo(structure: Any, name: str) -> None:
    try:
        with open(f"{name}.pickle", "wb") as file:
            pickle.dump(structure, file, protocol=4)
    except IOError:
        print(f"Error with saving {name}.pickle when trying to save {structure}")


search_memo: Dict[str, SpotifySearch] = get_memo("search")
album_tracks_memo: Dict[str, HasItems[SpotifyTrack]] = get_memo("tracks")
feature_memo: Dict[str, SpotifyFeatures] = get_memo("features")


def cache(album_descriptions: List[AlbumDescription], sp: spotipy.Spotify) -> None:
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
        if q not in search_memo:
            missed[0] = True
            search_memo[q] = sp.search(query(title, artists), type="album", limit=50)
        album_id = find_album_id_from_search(search_memo[q], artists)
        if album_id is not None and album_id not in album_tracks_memo:
            missed[1] = True
            album_tracks_memo[album_id] = sp.album_tracks(album_id)
    if missed[0]:
        set_memo(search_memo, "search")
    if missed[1]:
        set_memo(album_tracks_memo, "tracks")

    songs = get_songs(album_descriptions, sp)
    for songs_chunk in util.chunks(iter(songs), 100):
        seenAllSongs = True
        song_links = [song["uri"] for song in songs_chunk]
        for link in song_links:
            if link not in feature_memo:
                seenAllSongs = False
        if not seenAllSongs:
            missed[2] = True
            feature_list = sp.audio_features(song_links)
            for uri, features in zip(song_links, feature_list):
                feature_memo[uri] = features

    if missed[2]:
        set_memo(feature_memo, "features")


def find_album_id_from_search(
    search: SpotifySearch, artists: List[str]
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


def album_from_title_artist(
    title: str, artists: List[str], sp: spotipy.Spotify
) -> Optional[Album]:
    """
    Return an album
    """
    q = query(title, artists)

    if q in search_memo:
        search_result = search_memo[q]
    else:
        search_result = sp.search(q, type="album", limit=50)
        print(f"Key error looking up the query {q}")

    album_id = find_album_id_from_search(search_result, artists)
    if album_id:
        try:
            tracks = album_tracks_memo[album_id]
        except KeyError:
            tracks = sp.album_tracks(album_id)
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


def get_songs(
    album_descriptions: List[AlbumDescription], sp: spotipy.Spotify
) -> List[Song]:
    """
    Given a list of albums, find all the songs in those albums according to Spotify.
    """
    songs = []
    for title, artistList in album_descriptions:
        result = album_from_title_artist(title, artistList, sp)

        if not result:
            continue

        title, id, artists, tracks = result

        songs.extend(tracks)

    return songs


def add_audio_features(songs: List[Song], sp: spotipy.Spotify) -> List[Song]:
    if not songs:
        return []

    annotated_songs = []
    feature_list = []
    for song in songs:
        if song["uri"] in feature_memo:
            features = feature_memo[song["uri"]]
        else:
            features = sp.audio_features(song["uri"])[0]
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

    return annotated_songs


def filter_songs(feel: Feel, songs: List[Song], n: int = 25) -> List[Song]:
    # Find the N songs closest to the given feel, measured by the L2 distance.
    def dist(x: Song) -> float:
        song_feel = x["features"]
        diff = [
            feel["energy"] - song_feel["energy"],
            feel["dance"] - song_feel["dance"],
            feel["lyrics"] - song_feel["lyrics"],
            feel["valence"] - song_feel["valence"],
        ]
        return sum([d * d for d in diff])

    return heapq.nsmallest(n, songs, key=dist)


def create_playlist(
    songs: List[Song],
    sp: spotipy.Spotify,
    full_url: bool = True,
) -> str:
    # Find the watsong playlist and use it if possible
    playlist = sp.user_playlist_create(
        sp.current_user()["id"],
        "Watsong Playlist",
        public=False,
        collaborative=True,
        description="A playlist created by watsong just for you",
    )
    sp.playlist_add_items(playlist["id"], [song["uri"] for song in songs[:100]])
    # Unsubscribe from the playlist immediately. The user can subscribe later by hitting the
    # Subscribe button.
    sp.current_user_unfollow_playlist(playlist["id"])
    return (
        f'https://open.spotify.com/embed/playlist/{playlist["id"]}'
        if full_url
        else str(playlist["id"])
    )


def login(sp: spotipy.Spotify) -> Optional[Exception]:
    """
    Change who you are logged in as.
    """

    # removes cached account information
    try:
        os.remove(CACHE_PATH)
    except FileNotFoundError:
        pass

    # Make the login prompt appear by calling an api function
    sp.current_user()

    return None


def get_album_features(ids: List[str]) -> Dict[str, float]:
    """
    Given a list of playlist/album ids find the net average
    feature data (acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo) for the entire collection of songs in the playlists/albums
    """

    all_features: Dict[str, List[float]] = {
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
        "tempo": [],
    }

    sp = get_spotify()

    for id in ids:
        songsPerTrack = sp.album_tracks(id)["items"]

        for song in songsPerTrack:
            featuresForSong = sp.audio_features(song["uri"])

            for feature_type in featuresForSong[0].keys():
                if feature_type in all_features.keys():
                    value_of_feature = featuresForSong[0][feature_type]
                    all_features[feature_type].append(value_of_feature)

    avg_features = {}
    for (feature_name, values) in all_features.items():
        avg_features[feature_name] = sum(values) / len(values)

    return avg_features


def get_playlist_features(ids: List[str]) -> Dict[str, float]:
    all_features: Dict[str, List[float]] = {
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
        "tempo": [],
    }

    sp = get_spotify()

    for id in ids:
        songsPerTrack = sp.playlist_tracks(id)["items"]

        for song in songsPerTrack:
            featuresForSong = sp.audio_features(song["track"]["uri"])

            for feature_type in featuresForSong[0].keys():
                if feature_type in all_features.keys():
                    value_of_feature = featuresForSong[0][feature_type]
                    all_features[feature_type].append(value_of_feature)

    avg_features = {}
    for (feature_name, values) in all_features.items():
        avg_features[feature_name] = sum(values) / len(values)

    return avg_features


"""Return count album ids which are the most popular and relevant to the input query"""


def get_album_ids(query: str, count: int) -> List[str]:
    sp = get_spotify()
    result = sp.search(query, count, type="album")

    ids = []
    for playlist in result["albums"]["items"]:
        ids.append(playlist["id"])

    return ids


def get_playlist_ids(query: str, count: int) -> List[str]:
    """
    Return count playlist ids which are the most popular and relevant to the input query

    Note @param count can be max 50
    """

    sp = get_spotify()
    result = sp.search(query, count, type="playlist")

    ids = []
    for playlist in result["playlists"]["items"]:
        ids.append(playlist["id"])

    return ids


def average_of_album_playlist_features(
    album_features: Dict[str, float],
    playlist_features: Dict[str, float],
) -> Dict[str, Optional[float]]:
    average_features: Dict[str, Optional[float]] = {
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
        "tempo": None,
    }

    if len(set(album_features.keys()).difference(set(playlist_features.keys()))) == 0:
        feature_types = album_features.keys()

        for feature_name in feature_types:
            average_features[feature_name] = (
                album_features[feature_name] + playlist_features[feature_name]
            ) / 2

    return average_features


def subscribe_to_playlist(id: str, sp: spotipy.Spotify) -> None:
    """
    Take the current playlist and save it so that it isn't overwritten later.
    """
    sp.current_user_follow_playlist(id)


def get_song_features_from_query(query: str, sp: spotipy.Spotify) -> Dict[str, float]:
    all_features = {
        "danceability": 0.0,
        "energy": 0.0,
        "speechiness": 0.0,
        "acousticness": 0.0,
        "instrumentalness": 0.0,
        "liveness": 0.0,
        "valence": 0.0,
        "tempo": 0.0,
    }

    result = sp.search(query, type="track", limit=10)

    tracks = result["tracks"]["items"]
    numSongs = len(tracks)

    for song in tracks:
        track_features = sp.audio_features(song["uri"])[0]

        for feature in all_features:
            all_features[feature] = all_features[feature] + track_features[feature]

    for feature in all_features:
        all_features[feature] = all_features[feature] / numSongs

    return all_features


if __name__ == "__main__":
    album_list = [
        AlbumDescription("A girl between worlds", []),
    ]
    sp = get_spotify()
    album_songs = get_songs(album_list, sp)
    add_audio_features(album_songs, sp)
    x = create_playlist(album_songs, sp, full_url=False)
    subscribe_to_playlist(x, sp)
    print(x)
