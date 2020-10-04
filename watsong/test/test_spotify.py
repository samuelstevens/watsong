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
    link2 = create_playlist(songs)
    # TODO: Change lyrics and melody values when making those additionsblack

    assert link1 == link2
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

    assert filter_songs(empty_feel, arbitrary_song)


def test_filter_songs_not_enough_dance() -> None:
    empty_feel = Feel(dance=0.8, energy=0, valence=0, lyrics=0)
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

    assert not filter_songs(empty_feel, arbitrary_song)


def test_filter_songs_not_enough_energy() -> None:
    empty_feel = Feel(dance=0, energy=0.7, valence=0, lyrics=0)
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

    assert not filter_songs(empty_feel, arbitrary_song)
