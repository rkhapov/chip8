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

    def vx(self):
        return self.arg_registers[0]

    def vy(self):
        return self.arg_registers[1]


# JumpInstruction - class to determinate instruction is instruction which change PC
class JumpInstruction(Instruction):
    pass
