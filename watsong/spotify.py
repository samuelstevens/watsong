"""
This file is a starter for whatever Spotify stuff needs to happen
"""

from typing import List

from .structures import Album, Song, Result


def get_songs(albums: List[Album]) -> Result[List[Song]]:
    """
    Given a list of albums, find all the songs in those albums according to Spotify.
    """
    # some hardcoded results
    songs = [
        {
            "song": "Under the Boardwalk",
            "album": "Under the Boardwalk",
            "artist": "The Drifters",
        },
        {
            "song": "What's Love Got to Do with It",
            "album": "Private Dancer",
            "artist": "Tina Turner",
        },
        {
            "song": "This Is The Life",
            "album": "This Is The Life",
            "artist": "Amy Macdonald",
        },
        {
            "song": "I'll Wait",
            "album": "Golden Hour",
            "artist": "Sasha Sloan, Kygo",
        },
    ]

    return songs, None