from typing import Iterator, List
from .structures import T


def chunks(elements: Iterator[T], n: int) -> Iterator[List[T]]:
    """
    Yield successive n-sized chunks from elements.
    """
    at_end = False

    while not at_end:
        chunk = []
        for i in range(n):
            try:
                chunk.append(next(elements))
            except StopIteration:
                at_end = True
                break

        yield chunk
