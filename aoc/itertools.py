from collections.abc import Iterator
from collections import deque


def last(iterable):
    """Get the last value from `iterable`."""
    return deque(iterable, maxlen=1).pop()


def minmax(iterable):
    if isinstance(iterable, Iterator):
        iterable = list(iterable)
    return min(iterable), max(iterable)
