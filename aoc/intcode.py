from collections import deque
from copy import copy
from enum import Enum

import attr


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class OpCodes(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    HALT = 99


@attr.s(repr=False)
class Entry:
    state = attr.ib()
    parameter_mode = attr.ib()
    value = attr.ib()

    def write(self, value):
        if self.parameter_mode is ParameterMode.IMMEDIATE:
            raise RuntimeError('This parameter is in immediate mode.')
        self.state.memory[self.value] = value

    def read(self):
        if self.parameter_mode is ParameterMode.IMMEDIATE:
            return self.value
        return self.state.memory[self.value]

    def __repr__(self):
        cls = type(self)
        return f'<{cls.__name__} {self.parameter_mode._name_} {self.value}>'


def values(*parameters):
    """Convenience function for reading several parameters"""
    for p in parameters:
        yield p.read()


@attr.s
class Machine:
    memory = attr.ib()
    pos = attr.ib(default=0)
    _parameter_modes = attr.ib(init=False, factory=deque)
    input = attr.ib(factory=list, converter=iter)

    def read_opcode(self):
        value = str(self.memory[self.pos])
        self.pos += 1
        opcode = int(value[-2:])

        for mode in map(int, value[:-2]):
            self._parameter_modes.append(ParameterMode(mode))

        return OpCodes(opcode)

    def peek(self):
        return self.memory[self.pos]

    def read_arg(self):
        return next(self.read_args(1))

    def read_args(self, num_args):
        args = self.memory[self.pos:self.pos + num_args]
        self.pos += num_args

        for arg in args:
            try:
                mode = self._parameter_modes.pop()
            except IndexError:
                mode = ParameterMode.POSITION

            yield Entry(state=self, parameter_mode=mode, value=arg)

    def run(self):
        for output in self.run_generator():
            print(output)

    def run_single_output(self):
        for output in self.run_generator():
            assert self.peek() == OpCodes.HALT._value_
            return output

    def run_generator(self):
        while True:
            opcode = self.read_opcode()
            if opcode is OpCodes.ADD:
                p1, p2, p3 = self.read_args(3)
                a, b = values(p1, p2)
                p3.write(a + b)
            elif opcode is OpCodes.MULTIPLY:
                p1, p2, p3 = self.read_args(3)
                a, b = values(p1, p2)
                p3.write(a * b)
            elif opcode is OpCodes.INPUT:
                p1 = self.read_arg()
                try:
                    p1.write(next(self.input))
                except StopIteration:
                    raise RuntimeError('Expected input')
            elif opcode is OpCodes.OUTPUT:
                p1 = self.read_arg()
                yield p1.read()
            elif opcode is OpCodes.JUMP_IF_TRUE:
                p1, p2 = self.read_args(2)
                a, b = values(p1, p2)
                if a != 0:
                    self.pos = b
            elif opcode is OpCodes.JUMP_IF_FALSE:
                p1, p2 = self.read_args(2)
                a, b = values(p1, p2)
                if a == 0:
                    self.pos = b
            elif opcode is OpCodes.LESS_THAN:
                p1, p2, p3 = self.read_args(3)
                a, b = values(p1, p2)
                p3.write(1 if a < b else 0)
            elif opcode is OpCodes.EQUAL:
                p1, p2, p3 = self.read_args(3)
                a, b = values(p1, p2)
                p3.write(1 if a == b else 0)
            elif opcode is OpCodes.HALT:
                break
