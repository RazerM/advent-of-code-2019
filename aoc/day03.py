from enum import Enum

import attr

from .registry import register


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


@attr.s(repr=False)
class Move:
    direction = attr.ib()
    distance = attr.ib()

    def __repr__(self):
        return f'<Move {self.direction._value_}{self.distance}>'

    def __attrs_post_init__(self):
        self.direction_vector = self._get_direction_vector()

    def _get_direction_vector(self):
        if self.direction is Direction.UP:
            return Vector(0, 1)
        elif self.direction is Direction.DOWN:
            return Vector(0, -1)
        elif self.direction is Direction.LEFT:
            return Vector(-1, 0)
        elif self.direction is Direction.RIGHT:
            return Vector(1, 0)
        else:
            raise RuntimeError('Unreachable!')


@attr.s(frozen=True)
class Vector:
    x = attr.ib()
    y = attr.ib()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return NotImplemented


def parse_move(s):
    direction, distance = s[:1], s[1:]
    return Move(Direction(direction), int(distance))


@register(day=3)
def solve(file, verbose):
    wires = (
        [parse_move(move) for move in line.strip().split(',')]
        for line in file
    )

    positions = []
    intersection_steps = []

    for i, wire in enumerate(wires):
        positions.append(set())
        intersection_steps.append(dict())

        pos = Vector(0, 0)
        positions[i].add(pos)
        steps = 0

        for move in wire:
            for _ in range(move.distance):
                steps += 1
                pos += move.direction_vector
                positions[i].add(pos)
                intersection_steps[i][pos] = steps

    intersections = positions[0].intersection(*positions[1:])
    intersections.remove(Vector(0, 0))

    closest_intersection_dist = min(abs(p.x) + abs(p.y) for p in intersections)
    print('Part 1:', closest_intersection_dist)

    fewest_combined_steps = min(
        sum(s[intersection] for s in intersection_steps)
        for intersection in intersections
    )
    print('Part 2:', fewest_combined_steps)
