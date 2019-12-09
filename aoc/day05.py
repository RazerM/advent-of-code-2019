from .intcode import Machine, OpCodes, parse_opcodes
from .registry import register


def compute(opcodes, *, system_id):
    machine = Machine(opcodes, input=[system_id])

    diagnostic = None

    for output in machine.run_generator():
        if machine.peek() == OpCodes.HALT.value:
            diagnostic = output
        elif output != 0:
            raise RuntimeError('Test failed!')

    return diagnostic


@register(day=5)
def solve(file, verbose):
    opcodes = parse_opcodes(file)

    print('Part 1:', compute(opcodes, system_id=1))
    print('Part 2:', compute(opcodes, system_id=5))
