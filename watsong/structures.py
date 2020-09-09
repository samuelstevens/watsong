from typing import NamedTuple, List, Tuple, TypeVar, Optional

T = TypeVar("T")

Result = Tuple[T, Optional[Exception]]

Song = NamedTuple("Song", [("title", str)])

Album = NamedTuple(
    "Album",
    [
        ("title", str),
        ("spotify_id", str),
        ("artists", List[str]),
        ("songs", List[Song]),
    ],
)
