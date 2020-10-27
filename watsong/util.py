from typing import Iterator, List, TypeVar

T = TypeVar("T")


def chunks(elements: Iterator[T], n: int) -> Iterator[List[T]]:
    """
    Yield successive n-sized chunks from elements.
    """

    while True:
        chunk = []
        for i in range(n):
            try:
                chunk.append(next(elements))
            except StopIteration:
                yield chunk
                return

        yield chunk
