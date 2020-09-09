from typing import List, NamedTuple, Tuple

from .structures import Album, Result


def get_albums(query: str) -> Result[List[Album]]:
    return [], None