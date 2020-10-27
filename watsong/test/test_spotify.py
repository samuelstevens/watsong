import re

from ..spotify import add_audio_features, create_playlist, filter_songs, get_songs
from ..structures import AlbumDescription, Feel, Song
from .spotify_mocks import SpotifyMockMaker


def test_get_songs_many_songs_without_features() -> None:
    album_list = [
        AlbumDescription("A girl between worlds", ["Fatima Yamaha"]),
    ]
    mock = SpotifyMockMaker.between_worlds_mock()
    songs = get_songs(album_list, sp=mock)
    mock.search.assert_called_with("A girl between worlds", limit=50, type="album")
    mock.album_tracks.assert_called_with("4MGNcuX4Vvhv2hhn1FwtDW")

    assert songs[0] == {
        "title": "Between Worlds",
        "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
        "features": {},
        "artists": ["Fatima Yamaha"],
    }

    assert len(songs) == 7


def test_get_songs_many_songs_with_features() -> None:
    album_list = [
        AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
    ]
    mock = SpotifyMockMaker.between_worlds_mock()
    songs = get_songs(album_list, sp=mock)
    add_audio_features(songs, sp=mock)
    mock.audio_features.assert_called_with("spotify:track:6ezatiaJEBHpi72EjnTl9s")
    assert songs[0] == {
        "title": "Between Worlds",
        "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
        "features": {
            "energy": 0.611,
            "dance": 0.75,
            "valence": 0.546,
            "lyrics": 0.0538,
        },
        "artists": ["Fatima Yamaha"],
    }

    assert len(songs) == 7


def test_create_playlist() -> None:
    album_list = [
        AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
    ]
    mock = SpotifyMockMaker.between_worlds_mock()
    songs = get_songs(album_list, sp=mock)
    link1 = create_playlist(songs, sp=mock)
    mock.playlist_add_items.assert_called()
    assert re.match("https://open.spotify.com/embed/playlist/*", link1)


def test_audio_features_no_songs() -> None:
    annotated_songs = add_audio_features([])

    assert len(annotated_songs) == 0


def test_filter_songs_empty_feel() -> None:
    empty_feel = Feel(dance=0, energy=0, valence=0, lyrics=0)
    arbitrary_song = Song(
        title="Harder (with Bebe Rexha)",
        uri="spotify:track:5ieQrVW2U70NFMg28mzlqC",
        features={
            "energy": 0.611,
            "dance": 0.75,
            "valence": 0.546,
            "lyrics": 0.0538,
        },
        artists=["Jax Jones", "Bebe Rexha"],
    )

    assert filter_songs(empty_feel, [arbitrary_song])


def test_filter_songs_no_feeling() -> None:
    empty_feel = Feel(dance=0, energy=0, valence=0, lyrics=0)
    songs_list = [
        Song(
            title=str(i),
            uri="test_data",
            features={
                "energy": i / 100,
                "dance": i / 100,
                "valence": i / 100,
                "lyrics": i / 100,
            },
            artists=[str(i)],
        )
        for i in range(100)
    ]

    filtered = filter_songs(empty_feel, songs_list, 10)
    assert len(filtered) == 10
    assert [song["title"] for song in filtered] == [str(i) for i in range(10)]


def test_filter_songs_choose_closer() -> None:
    songs_list = [
        Song(
            title=str(i),
            uri="test_data",
            features={
                "energy": i,
                "dance": i,
                "valence": i,
                "lyrics": i,
            },
            artists=[str(i)],
        )
        for i in range(2)
    ]

    filtered = filter_songs(
        Feel(dance=0.1, energy=1, valence=0.3, lyrics=0.1), songs_list, 1
    )
    assert len(filtered) == 1
    assert filtered[0]["title"] == "0"
    filtered = filter_songs(
        Feel(dance=0.8, energy=1, valence=0.8, lyrics=0.1), songs_list, 1
    )
    assert len(filtered) == 1
    assert filtered[0]["title"] == "1"
