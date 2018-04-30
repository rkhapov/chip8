#!/usr/bin/env python3


from abc import *
from virtualmachine.machine import Machine


class Instruction:
    def __init__(self):
        self.arg_registers = []
        self.arg_constant = None

    @abstractmethod
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def opcode_format() -> str:
        raise NotImplemented
