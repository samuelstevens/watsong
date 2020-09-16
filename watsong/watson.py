"""
This file is a starter for any Watson stuff that needs to happen.
"""

from typing import List

from structures import AlbumDescription, Result


def get_albums(query: str) -> Result[List[AlbumDescription]]:
    """
    Given a natural language query, use watson to return the best albums for that query.
    """
    return [], None
