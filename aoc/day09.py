from .intcode import Machine, parse_intcode
from .registry import register


@register(day=9)
def solve(file, verbose):
    intcode = parse_intcode(file)

    machine = Machine(intcode, input=[1])
    print('Part 1:', machine.run_single_output())

    machine = Machine(intcode, input=[2])
    print('Part 2:', machine.run_single_output())
