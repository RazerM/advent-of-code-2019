from itertools import groupby


def exactly_two_adjacent(iterable):
    for _, g in groupby(iterable):
        if sum(1 for _ in g) == 2:
            return True
    return False


def is_unique(seq):
    return len(set(seq)) == len(seq)


def is_sorted(seq):
    if not isinstance(seq, list):
        seq = list(seq)
    return seq == sorted(seq)


def check_valid1(password):
    chars = list(password)
    return is_sorted(chars) and not is_unique(chars)


def check_valid2(password):
    chars = list(password)
    return is_sorted(chars) and exactly_two_adjacent(chars)


def solve(file, verbose):
    lo, hi = map(int, file.read().split('-'))

    passwords = [str(p) for p in range(lo, hi + 1)]

    print('Part 1:', sum(1 for p in passwords if check_valid1(p)))
    print('Part 2:', sum(1 for p in passwords if check_valid2(p)))
