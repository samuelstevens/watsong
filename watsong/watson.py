"""
This file is a starter for any Watson stuff that needs to happen.
"""

from typing import List

from .structures import Album, Result


def get_albums(query: str) -> Result[List[Album]]:
    """
    Given a natural language query, use watson to return the best albums for that query.
    """
    return [], None