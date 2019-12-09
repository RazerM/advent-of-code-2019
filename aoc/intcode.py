import inspect
from collections import deque
from enum import Enum
from itertools import repeat
from math import floor, log10

import attr


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class OpCodes(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    ADJUST_RELATIVE_BASE = 9
    HALT = 99


@attr.s(repr=False)
class Entry:
    machine = attr.ib()
    parameter_mode = attr.ib()
    value = attr.ib()

    def write(self, value):
        if self.parameter_mode is ParameterMode.IMMEDIATE:
            raise RuntimeError('This parameter is in immediate mode.')

        position = self.value

        if self.parameter_mode is ParameterMode.RELATIVE:
            position += self.machine._relative_base

        self.machine.memory[position] = value

    def read(self):
        if self.parameter_mode is ParameterMode.IMMEDIATE:
            return self.value

        position = self.value

        if self.parameter_mode is ParameterMode.RELATIVE:
            position += self.machine._relative_base

        return self.machine.memory[position]

    def __repr__(self):
        cls = type(self)
        return f'<{cls.__name__} {self.parameter_mode._name_} {self.value}>'


def values(*parameters):
    """Convenience function for reading several parameters"""
    for p in parameters:
        yield p.read()


class GrowableList(list):
    def _grow(self, item):
        if isinstance(item, slice) and item.stop is not None:
            upper = item.stop
        elif isinstance(item, int):
            upper = item + 1
        else:
            return

        if upper > len(self):
            self.extend(repeat(0, times=upper - len(self)))

    def __getitem__(self, item):
        self._grow(item)
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        self._grow(key)
        super().__setitem__(key, value)


class Halt(Exception):
    """Raised when the machine should halt."""


def implements(opcode):
    def decorator(fn):
        fn._implements_opcode = opcode
        return fn
    return decorator


def register_opcode_funcs(cls):
    for _, fn in inspect.getmembers(cls, inspect.isfunction):
        try:
            opcode = fn._implements_opcode
        except AttributeError:
            continue

        del fn._implements_opcode
        cls._opcode_funcs[opcode] = fn

    return cls


@attr.s
@register_opcode_funcs
class Machine:
    # Using GrowableList means input is always copied
    memory = attr.ib(converter=GrowableList)
    pos = attr.ib(default=0)
    input = attr.ib(factory=list, converter=iter)
    _parameter_modes = attr.ib(init=False, factory=deque)
    _relative_base = attr.ib(init=False, default=0)
    _opcode_funcs = dict()

    def read_opcode(self):
        value = self.memory[self.pos]
        self.pos += 1
        opcode = value % 100

        for p in range(floor(log10(value)), 1, -1):
            self._parameter_modes.append(ParameterMode(value // 10 ** p % 10))

        return OpCodes(opcode)

    def _run_opcode(self, opcode):
        return self._opcode_funcs[opcode](self)

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

            yield Entry(machine=self, parameter_mode=mode, value=arg)

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
            try:
                output = self._run_opcode(opcode)
            except Halt:
                break
            else:
                if output is not None:
                    yield output

    @implements(OpCodes.ADD)
    def _add(self):
        p1, p2, p3 = self.read_args(3)
        a, b = values(p1, p2)
        p3.write(a + b)

    @implements(OpCodes.MULTIPLY)
    def _multiply(self):
        p1, p2, p3 = self.read_args(3)
        a, b = values(p1, p2)
        p3.write(a * b)

    @implements(OpCodes.INPUT)
    def _input(self):
        p1 = self.read_arg()
        try:
            p1.write(next(self.input))
        except StopIteration:
            raise RuntimeError('Expected input')

    @implements(OpCodes.OUTPUT)
    def _output(self):
        p1 = self.read_arg()
        return p1.read()

    @implements(OpCodes.JUMP_IF_TRUE)
    def _jump_if_true(self):
        p1, p2 = self.read_args(2)
        a, b = values(p1, p2)
        if a != 0:
            self.pos = b

    @implements(OpCodes.JUMP_IF_FALSE)
    def _jump_if_false(self):
        p1, p2 = self.read_args(2)
        a, b = values(p1, p2)
        if a == 0:
            self.pos = b

    @implements(OpCodes.LESS_THAN)
    def _less_than(self):
        p1, p2, p3 = self.read_args(3)
        a, b = values(p1, p2)
        p3.write(1 if a < b else 0)

    @implements(OpCodes.EQUAL)
    def _equal(self):
        p1, p2, p3 = self.read_args(3)
        a, b = values(p1, p2)
        p3.write(1 if a == b else 0)

    @implements(OpCodes.ADJUST_RELATIVE_BASE)
    def _adjust_relative_base(self):
        p1 = self.read_arg()
        self._relative_base += p1.read()

    @implements(OpCodes.HALT)
    def _halt(self):
        raise Halt


def parse_opcodes(file):
    data = ''.join(line.strip() for line in file)
    return [int(x) for x in data.split(',')]
