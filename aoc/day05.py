from .intcode import Machine, OpCodes, parse_intcode
from .registry import register


def compute(intcode, *, system_id):
    machine = Machine(intcode, input=[system_id])

    diagnostic = None

    for output in machine.run_generator():
        if machine.peek() == OpCodes.HALT.value:
            diagnostic = output
        elif output != 0:
            raise RuntimeError('Test failed!')

    return diagnostic


@register(day=5)
def solve(file, verbose):
    intcode = parse_intcode(file)

    print('Part 1:', compute(intcode, system_id=1))
    print('Part 2:', compute(intcode, system_id=5))
