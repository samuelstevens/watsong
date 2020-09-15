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
        Song(title="Under the Boardwalk"),
        Song(title="What's Love Got to Do with It"),
        Song(title="This Is The Life"),
        Song(title="I'll Wait"),
        Song(title="Under the Boardwalk"),
    ]

    return songs, None