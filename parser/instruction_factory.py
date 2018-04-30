#!/usr/bin/env python3

from instructions.cls_instruction import ClsInstruction
from parser.opcode_formatter import *
from virtualmachine.instruction import Instruction
from parser.opcode_unit import *


class InstructionFactory:
    def __init__(self):
        self._opcode_formatter = OpcodeFormatter()
        self._instructions = InstructionFactory._get_instructions_list()
        self._cache = dict()

    def from_opcode(self, opcode: bytearray) -> Instruction:
        if not isinstance(opcode, bytearray) and not isinstance(opcode, bytes):
            raise TypeError('opcode must be byte-sequence object')

        tupled = tuple(opcode)
        if tupled not in self._cache:
            self._cache[tupled] = self._get_instruction_by_opcode(opcode)

        return self._cache[tupled]

    def _get_instruction_by_opcode(self, opcode: bytearray):
        for instruction in self._instructions:
            if self._opcode_formatter.is_opcode_valid(opcode, instruction.opcode_format()):
                return self._create_instruction_from_opcode(instruction, opcode)

        raise NotImplemented('Unknown instruction {}'.format(list(map(hex, opcode))))

    def _create_instruction_from_opcode(self, instruction_type: type(Instruction), opcode: bytearray):
        instruction = instruction_type()

        opcode_units = self._opcode_formatter.parse_by_format(opcode, instruction_type.opcode_format())

        for unit in opcode_units:
            if unit.Type == OpcodeUnitType.REGISTER:
                instruction.arg_registers.append(unit.Value)

            if unit.Type == OpcodeUnitType.CONSTANT:
                instruction.arg_constant = unit.Value

        return instruction

    @staticmethod
    def _get_instructions_list():
        return [ClsInstruction]
