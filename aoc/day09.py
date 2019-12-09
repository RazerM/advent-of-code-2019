from copy import copy

from .intcode import Machine


def solve(file, verbose):
    data = ''.join(line.strip() for line in file)
    opcodes = [int(x) for x in data.split(',')]

    machine = Machine(copy(opcodes), input=[1])
    print('Part 1:', machine.run_single_output())

    machine = Machine(copy(opcodes), input=[2])
    print('Part 2:', machine.run_single_output())
