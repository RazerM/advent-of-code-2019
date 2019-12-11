from collections import defaultdict, deque
from itertools import cycle
from math import atan2, pi

from .registry import register
from .utils import Vector, normalize_angle


@register(day=10)
def solve(file, verbose):
    asteroids = set()

    for y, line in enumerate(file):
        for x, char in enumerate(line.strip()):
            if char == '#':
                asteroids.add(Vector(x, y))

    observed = defaultdict(set)
    byangle = defaultdict(lambda: defaultdict(deque))

    for station in asteroids:
        for asteroid in asteroids:
            if station == asteroid:
                continue

            rel = asteroid - station

            # rotate angle by 90° because the laser starts pointing up.
            angle = normalize_angle(atan2(rel.y, rel.x) + pi / 2, center=pi)
            observed[station].add(angle)
            byangle[station][angle].append(asteroid)

    best = max(observed.items(), key=lambda x: len(x[1]))
    print('Part 1:', len(best[1]))

    station = best[0]

    blasted = []

    for angle in cycle(sorted(byangle[station])):
        try:
            target = byangle[station][angle].popleft()
        except IndexError:
            continue

        blasted.append(target)

        if len(blasted) == 200:
            found = blasted[-1]
            print('Part 2:', found.x * 100 + found.y)
            break
