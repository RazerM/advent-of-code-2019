from .intcode import Machine, parse_opcodes
from .registry import register


@register(day=9)
def solve(file, verbose):
    opcodes = parse_opcodes(file)

    machine = Machine(opcodes, input=[1])
    print('Part 1:', machine.run_single_output())

    machine = Machine(opcodes, input=[2])
    print('Part 2:', machine.run_single_output())
