import collections


def last(iterable):
    """Get the last value from `iterable`."""
    return collections.deque(iterable, maxlen=1).pop()
