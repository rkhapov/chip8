#!/usr/bin/env python3

from parser.opcode_formatter import *
from parser.opcode_unit import *
from virtualmachine.instructions import *


class InstructionFactoryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


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

    def get_instructions_classes(self):
        return self._instructions

    def _get_instruction_by_opcode(self, opcode: bytearray):
        instructions = []

        for instruction in self._instructions:
            if self._opcode_formatter.is_opcode_valid(opcode, instruction.opcode_format()):
                instructions.append(instruction)

        if len(instructions) == 0:
            raise InstructionFactoryError('Unknown instruction {}'.format(list(map(hex, opcode))))

        if len(instructions) > 1:
            raise InstructionFactoryError('Ambigious opcode: {}'.format(list(map(hex, opcode))))

        return self._create_instruction_from_opcode(instructions[0], opcode)

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
        instruction_subclasses = [instr for instr in Instruction.__subclasses__() if instr != JumpInstruction]
        jump_subclasses = [instr for instr in JumpInstruction.__subclasses__()]

        return instruction_subclasses + jump_subclasses
