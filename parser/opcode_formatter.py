#!/usr/bin/env python3

"""
OpcodeFormatter - parse opcode by given formart
Usage format is:
 [0 - 9, A - F] for hex value
 [X, Y] - registers
 NNN - address
 NN - 8-bit constant
 N - 4-bit constant

raise OpcodeFormatError in case opcode does not correspond for format
"""

from parser.opcode_unit import *


class OpcodeFormatError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class OpcodeFormatter:
    def parse_by_format(self, opcode: bytearray, opcode_format: str):
        if not isinstance(opcode_format, str) or len(opcode_format) != 4:
            raise TypeError('format must have type string and be length of 4')

        if (not isinstance(opcode, bytearray) and not isinstance(opcode, bytes)) or len(opcode) != 2:
            raise TypeError('opcode must have type bytes and be length of 2')

        return OpcodeFormatter._parse(opcode, opcode_format.lower())

    def is_opcode_valid(self, opcode: bytearray, opcode_format: str):
        if not isinstance(opcode_format, str) or len(opcode_format) != 4:
            raise TypeError('format must have type string and be length of 4')

        if (not isinstance(opcode, bytearray) and not isinstance(opcode, bytes)) or len(opcode) != 2:
            raise TypeError('opcode must have type bytes and be length of 2')

        opcode_bytes = bytearray([(opcode[0] & 0xF0) >> 4, opcode[0] & 0x0F, (opcode[1] & 0xF0) >> 4, opcode[1] & 0x0F])

        return OpcodeFormatter._check_valid(opcode_bytes, opcode_format.lower())

    @staticmethod
    def _parse(opcode: bytearray, opcode_format: str):
        opcode_bytes = bytearray([(opcode[0] & 0xF0) >> 4, opcode[0] & 0x0F, (opcode[1] & 0xF0) >> 4, opcode[1] & 0x0F])

        if not OpcodeFormatter._check_valid(opcode_bytes, opcode_format):
            raise OpcodeFormatError('{} doesnt correspond to format {}'.format(opcode_bytes, opcode_format))

        opcode_units = []

        i = 0
        while i < 4:
            if opcode_format[i] in {'x', 'y'}:
                opcode_units.append(OpcodeUnit(OpcodeUnitType.REGISTER, opcode_bytes[i]))
                i += 1
                continue

            if opcode_format[i] != 'n':
                i += 1
                continue

            constant_bytes = bytearray()
            while i + len(constant_bytes) < 4 and opcode_format[i + len(constant_bytes)] == 'n':
                constant_bytes.append(opcode_bytes[i + len(constant_bytes)])

            value = 0
            for b in constant_bytes:
                value = (value << 4) | b

            opcode_units.append(OpcodeUnit(OpcodeUnitType.CONSTANT, value))

            i += len(constant_bytes)

        return opcode_units

    @staticmethod
    def _check_valid(opcode_bytes: bytearray, opcode_format: str):
        opcode_bytes = list(opcode_bytes)
        for i in range(4):
            if opcode_format[i] in {'x', 'y', 'n'}:
                continue

            if opcode_format[i] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}:
                raise OpcodeFormatError('Unexpected symbol: {}'.format(opcode_format[i]))

            if opcode_bytes[i] != int(opcode_format[i], 16):
                return False

        return True
