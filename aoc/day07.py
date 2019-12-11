from collections import deque
from itertools import permutations

from .intcode import Machine, parse_intcode
from .itertools import last
from .registry import register


def compute(intcode, phase_seq):
    value = 0

    for phase in phase_seq:
        machine = Machine(intcode, input=[phase, value])
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


def compute_feedback(intcode, phase_seq):
    signals = deque([0])

    machines = [
        Machine(intcode, input=machine_input(phase, signals))
        for phase in phase_seq
    ]

    generators = (machine_feedback(m, signals) for m in machines)
    final_outputs = last(zip(*generators))

    # Return the final output of the last machine.
    return final_outputs[-1]


@register(day=7)
def solve(file, verbose):
    intcode = parse_intcode(file)

    highest_signal = max(
        compute(intcode, phase_seq) for phase_seq in permutations(range(5))
    )

    print('Part 1:', highest_signal)

    highest_signal = max(
        compute_feedback(intcode, phase_seq)
        for phase_seq in permutations(range(5, 10))
    )

    print('Part 2:', highest_signal)
