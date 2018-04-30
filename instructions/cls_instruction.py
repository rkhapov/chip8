#!/usr/bin/env python3

from virtualmachine.instruction import Instruction
from virtualmachine.machine import Machine


class ClsInstruction(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '00E0'
