from itertools import groupby


def exactly_two_adjacent(iterable):
    for k, g in groupby(iterable):
        if sum(1 for _ in g) == 2:
            return True
    return False


def is_unique(seq):
    return len(set(seq)) == len(seq)


def is_sorted(seq):
    if not isinstance(seq, list):
        seq = list(seq)
    return seq == sorted(seq)


def part1(lo, hi):
    num = 0

    for x in range(lo, hi + 1):
        digits = list(str(x))
        if not is_sorted(digits):
            continue

        if is_unique(digits):
            continue

        num += 1

    return num


def part2(lo, hi):
    num = 0

    for i in range(lo, hi + 1):
        digits = list(str(i))

        if not is_sorted(digits):
            continue

        if not exactly_two_adjacent(digits):
            continue

        num += 1

    return num


def solve(file, verbose):
    lo, hi = map(int, file.read().split('-'))
    print('Part 1:', part1(lo, hi))
    print('Part 2:', part2(lo, hi))
