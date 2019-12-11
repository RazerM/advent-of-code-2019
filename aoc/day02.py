from itertools import product

from .intcode import Machine, parse_intcode
from .registry import register


def compute(intcode, *, noun, verb):
    machine = Machine(memory=intcode)
    machine.memory[1] = noun
    machine.memory[2] = verb

    machine.run()

    return machine.memory[0]


def part2(intcode):
    for noun, verb in product(range(100), range(100)):
        if compute(intcode, noun=noun, verb=verb) == 19690720:
            return 100 * noun + verb


@register(day=2)
def solve(file, verbose):
    intcode = parse_intcode(file)

    print('Part 1:', compute(intcode, noun=12, verb=2))
    print('Part 2:', part2(intcode))
