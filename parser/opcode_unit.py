"""
OpcodeUnit - class for representation of registers, constant, addresses at instructions
"""

from enum import Enum


class OpcodeUnitType(Enum):
    REGISTER = 1,
    CONSTANT = 2


class OpcodeUnit:
    def __init__(self, opcode_type: OpcodeUnitType, value: int):
        if not isinstance(opcode_type, OpcodeUnitType):
            raise TypeError('unit type must be OpcodeUnitType')

        if not isinstance(value, int):
            raise TypeError('value of opcode unit must be integer')

        if opcode_type == OpcodeUnitType.REGISTER:
            value = value % 16

        self.Type = opcode_type
        self.Value = value

    def __eq__(self, other):
        if not isinstance(other, OpcodeUnit):
            return False

        return self.Type == other.Type and self.Value == other.Value
