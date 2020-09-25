# This file name doesn't start with test_ so that it doesn't run automatically,
# since it requires some credentials to be filled out on behalf of the user.
# Test with python -m unittest watsong.test.spotify
import sys
import unittest

sys.path.append("..")  # Adds higher directory to python modules path.

from watsong.spotify import get_songs, add_audio_features, create_playlist
from watsong.structures import AlbumDescription


# TODO: Once Sam finalizes the filter songs API, unit tests need to be made for it


class TestSpotify(unittest.TestCase):
    def test_get_songs_single_artist_many_songs_without_features(self) -> None:
        album_list = [
            AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
        ]
        songs, errors = get_songs(album_list)

        self.assertEqual(
            songs[0],
            {
                "title": "Between Worlds",
                "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
                "features": {},
            },
        )
        self.assertEqual(len(songs), 7)
        self.assertIsNone(errors)

    def test_get_songs_single_artist_many_songs_with_features(self) -> None:
        album_list = [
            AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
        ]
        songs, errors = get_songs(album_list)
        add_audio_features(songs)

        # TODO: Change lyrics and melody values when making those additions
        self.assertEqual(
            songs[0],
            {
                "title": "Between Worlds",
                "uri": "spotify:track:0Vpdt3FsW8m7nC4FDk3rfw",
                "features": {"energy": 0.611, "dance": 0.75, "lyrics": 0, "melody": 0},
            },
        )
        self.assertEqual(len(songs), 7)
        self.assertIsNone(errors)

    def test_get_songs_multi_artist_one_song_without_features(self) -> None:
        album_list = [
            AlbumDescription("Harder", ["Jax Jones", "Bebe Rexha"]),
        ]
        songs, errors = get_songs(album_list)

        self.assertEqual(
            songs[0],
            {
                "title": "Harder (with Bebe Rexha)",
                "uri": "spotify:track:5ieQrVW2U70NFMg28mzlqC",
                "features": {},
            },
        )
        self.assertEqual(len(songs), 1)

    def test_create_playlist(self) -> None:
        album_list = [
            AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
        ]
        songs, errors = get_songs(album_list)
        link = create_playlist(songs)
        link2 = create_playlist(songs)
        # TODO: Change lyrics and melody values when making those additionsblack
        self.assertEqual(link, link2)
        self.assertRegex(link, "https://open.spotify.com/embed/playlist/*")


if __name__ == "__main__":
    unittest.main()
