from functools import reduce

import numpy as np
from more_itertools import chunked


combine = np.vectorize(lambda a, b: b if a == 2 else a)


def count_n(arr, n):
    """Count occurrences of `n` in `arr`."""
    return np.count_nonzero(arr == n)


def get_layers(digits, *, width, height):
    return [
        np.array(l).reshape(height, width)
        for l in chunked(digits, width * height)
    ]


def solve(file, verbose):
    digits = (int(c) for c in file.read().strip())

    layers = get_layers(digits, width=25, height=6)

    fewest_zeros = min(layers, key=lambda l: count_n(l, 0))
    print('Part 1:', count_n(fewest_zeros, 1) * count_n(fewest_zeros, 2))

    combined = reduce(combine, layers)

    print('Part 2:')
    for row in combined:
        for col in row:
            print('#' if col == 1 else ' ', end='')
        print()
