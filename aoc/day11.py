from more_itertools import chunked

from .intcode import Machine, parse_intcode
from .itertools import minmax
from .registry import register
from .utils import Vector


def turn_left(v):
    return Vector(v.y, -v.x)


def turn_right(v):
    return Vector(-v.y, v.x)


def paint_robot(intcode, *, start_color):
    pos = Vector(0, 0)

    #       -y
    #       ^
    #       |
    # -x <--+--> +x
    #       |
    #       v
    #       +y

    # robot starts facing up
    direction = Vector(0, -1)

    colors = dict()
    colors[pos] = start_color

    def current_color():
        while True:
            yield colors.get(pos, 0)

    m = Machine(intcode, input=current_color())

    for paint, turn in chunked(m.run_generator(),2):
        if paint == 0:
            colors[pos] = 0
        elif paint == 1:
            colors[pos] = 1
        else:
            raise RuntimeError

        if turn == 0:
            direction = turn_left(direction)
        elif turn == 1:
            direction = turn_right(direction)
        else:
            raise RuntimeError

        pos += direction

    return colors


@register(day=11)
def solve(file, verbose):
    intcode = parse_intcode(file)

    colors = paint_robot(intcode, start_color=0)
    print('Part 1:', len(colors))

    colors = paint_robot(intcode, start_color=1)

    xmin, xmax = minmax(v.x for v in colors)
    ymin, ymax = minmax(v.y for v in colors)

    print('Part 2:')
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            c = colors.get(Vector(x, y), 0)
            print('#' if c == 1 else ' ', end='')
        print()
