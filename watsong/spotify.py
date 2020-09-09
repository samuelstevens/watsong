from typing import List

from .structures import Album, Song, Result


def get_songs(albums: List[Album]) -> Result[List[Song]]:
    return [], None