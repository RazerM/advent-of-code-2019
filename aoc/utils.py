from math import floor, pi, tau

import attr


@attr.s(frozen=True)
class Vector:
    x = attr.ib()
    y = attr.ib()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        return NotImplemented


def normalize_angle(theta, center=0):
    return theta - tau * floor((theta + pi - center) / tau)
