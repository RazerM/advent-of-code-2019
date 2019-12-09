from itertools import product

from .intcode import Machine, parse_opcodes
from .registry import register


def compute(opcodes, *, noun, verb):
    machine = Machine(memory=opcodes)
    machine.memory[1] = noun
    machine.memory[2] = verb

    machine.run()

    return machine.memory[0]


def part2(opcodes):
    for noun, verb in product(range(100), range(100)):
        if compute(opcodes, noun=noun, verb=verb) == 19690720:
            return 100 * noun + verb


@register(day=2)
def solve(file, verbose):
    opcodes = parse_opcodes(file)

    print('Part 1:', compute(opcodes, noun=12, verb=2))
    print('Part 2:', part2(opcodes))
