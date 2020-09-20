import unittest
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from watsong.spotify import get_songs
from watsong.structures import AlbumDescription


class TestSpotify(unittest.TestCase):
    def test_get_songs_single_artist_many_songs(self) -> None:
        album_list = [
            AlbumDescription("A girl between two worlds", ["Fatima Yamaha"]),
        ]
        songs, errors = get_songs(album_list)

        self.assertEqual(songs[0], {"title": "Between Worlds"})
        self.assertEqual(len(songs), 7)
        self.assertIsNone(errors)

    def test_get_songs_multi_artist_one_song(self) -> None:
        album_list = [
            AlbumDescription("Harder", ["Jax Jones", "Bebe Rexha"]),
        ]
        songs, errors = get_songs(album_list)

        self.assertEqual(songs[0], {"title": "Harder (with Bebe Rexha)"})
        self.assertEqual(len(songs), 1)


if __name__ == "__main__":
    unittest.main()
