import unittest
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from watsong.spotify import get_songs, add_audio_features
from watsong.structures import AlbumDescription


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

        # TODO: Change lyrics and melody values when making those additionsblack
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


if __name__ == "__main__":
    unittest.main()
