import re

from ..spotify import add_audio_features, create_playlist, filter_songs, get_songs
from ..structures import AlbumDescription, Feel, Song


def test_get_songs_single_artist_many_songs_without_features() -> None:
    album_list = [
        AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
    ]
    songs, error = get_songs(album_list)

    assert songs[0] == {
        "title": "Between Worlds",
        "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
        "features": {},
        "artists": ["Fatima Yamaha"],
    }

    assert len(songs) == 7
    assert error is None


def test_get_songs_single_artist_many_songs_with_features() -> None:
    album_list = [
        AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
    ]
    songs, error = get_songs(album_list)
    add_audio_features(songs)

    # TODO: Change lyrics and melody values when making those additions
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
    assert error is None


def test_get_songs_multi_artist_one_song_without_features() -> None:
    album_list = [
        AlbumDescription("Harder", ["Jax Jones", "Bebe Rexha"]),
    ]
    songs, error = get_songs(album_list)

    assert songs[0] == {
        "title": "Harder (with Bebe Rexha)",
        "uri": "spotify:track:5ieQrVW2U70NFMg28mzlqC",
        "features": {},
        "artists": ["Jax Jones", "Bebe Rexha"],
    }
    assert len(songs) == 1
    assert error is None


def test_create_playlist() -> None:
    album_list = [
        AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
    ]
    songs, errors = get_songs(album_list)
    link1 = create_playlist(songs)

    assert re.match("https://open.spotify.com/embed/playlist/*", link1)


def test_audio_features_no_songs() -> None:
    annotated_songs, err = add_audio_features([])

    assert len(annotated_songs) == 0
    assert err is None


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
