from collections import deque
from copy import copy
from itertools import permutations

from .intcode import Machine
from .itertools import last
from .registry import register


def compute(opcodes, phase_seq):
    value = 0

    for phase in phase_seq:
        machine = Machine(copy(opcodes), input=[phase, value])
        value = machine.run_single_output()

    return value


def machine_input(phase, signals):
    """Yields the `phase` to initalise the machine, then pops items off of the
    shared `signals` deque.
    """
    yield phase
    while True:
        yield signals.pop()


def machine_feedback(machine, signals):
    """Gets one output from `machine` and appends it to `signals` before
    yielding.
    """
    for output in machine.run_generator():
        # Add output to the signals deque so the next machine gets it as input
        signals.append(output)

        # Yield so the next machine can run
        yield output


def compute_feedback(opcodes, phase_seq):
    signals = deque([0])

    machines = [
        Machine(copy(opcodes), input=machine_input(phase, signals))
        for phase in phase_seq
    ]

    generators = (machine_feedback(m, signals) for m in machines)
    final_outputs = last(zip(*generators))

    # Return the final output of the last machine.
    return final_outputs[-1]


@register(day=7)
def solve(file, verbose):
    data = ''.join(line.strip() for line in file)
    opcodes = [int(x) for x in data.split(',')]

    highest_signal = max(
        compute(opcodes, phase_seq) for phase_seq in permutations(range(5))
    )

    print('Part 1:', highest_signal)

    highest_signal = max(
        compute_feedback(opcodes, phase_seq)
        for phase_seq in permutations(range(5, 10))
    )

    print('Part 2:', highest_signal)
