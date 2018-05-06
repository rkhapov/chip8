import unittest
from parser.opcode_formatter import *
from parser.opcode_unit import *


class OpcodeFormatterTests(unittest.TestCase):
    def test_is_opcode_valid(self):
        of = OpcodeFormatter()

        self.assertTrue(of.is_opcode_valid(bytearray([0xAA, 0xAA]), 'AAAA'))
        self.assertTrue(of.is_opcode_valid(bytearray([0xAF, 0xAC]), 'AFAC'))
        self.assertTrue(of.is_opcode_valid(bytearray([0x5F, 0x1C]), '5F1C'))
        self.assertTrue(of.is_opcode_valid(bytearray([0x5F, 0x1C]), '5FNN'))
        self.assertTrue(of.is_opcode_valid(bytearray([0x5F, 0x1C]), 'XYNN'))
        self.assertTrue(of.is_opcode_valid(bytearray([0x12, 0x34]), '1234'))
        self.assertTrue(of.is_opcode_valid(bytearray([0xBB, 0xC1]), 'NNN1'))

        self.assertFalse(of.is_opcode_valid(bytearray([0xBB, 0xAC]), 'AAAA'))
        self.assertFalse(of.is_opcode_valid(bytearray([0x1A, 0xAC]), '2AXY'))
        self.assertFalse(of.is_opcode_valid(bytearray([0x1A, 0xA1]), '2AXY'))
        self.assertFalse(of.is_opcode_valid(bytearray([0xBB, 0x32]), 'NN12'))

    def test_parse_by_format_invalid_format_should_raise_exception(self):
        of = OpcodeFormatter()

        def parse_action(opcode, format):
            return of.parse_by_format(opcode, format)

        self.assertRaises(OpcodeFormatError, parse_action, bytearray([0xBB, 0xAC]), 'AAAA')
        self.assertRaises(OpcodeFormatError, parse_action, bytearray([0x1A, 0xAC]), '2AXY')
        self.assertRaises(OpcodeFormatError, parse_action, bytearray([0x1A, 0xA1]), '2AXY')
        self.assertRaises(OpcodeFormatError, parse_action, bytearray([0xBB, 0xC2]), 'NNN1')
        self.assertRaises(OpcodeFormatError, parse_action, bytearray([0xBB, 0x32]), 'NN12')

    @staticmethod
    def _parse_by_format_tests():
        of = OpcodeFormatter()

        yield of.parse_by_format(bytearray([0x21, 0x11]), '2111'), []

        yield of.parse_by_format(bytearray([0x11, 0x11]), '111Y'), [OpcodeUnit(OpcodeUnitType.REGISTER, 1)]

        yield of.parse_by_format(bytearray([0x11, 0xA1]), '11Y1'), [OpcodeUnit(OpcodeUnitType.REGISTER, 0xA)]

        yield of.parse_by_format(bytearray([0x11, 0x11]), 'X111'), [OpcodeUnit(OpcodeUnitType.REGISTER, 1)]

        yield of.parse_by_format(bytearray([0x21, 0x11]), 'NNNN'), [OpcodeUnit(OpcodeUnitType.CONSTANT, 0x2111)]

        yield of.parse_by_format(bytearray([0xAC, 0x1B]), 'XY1N'), [OpcodeUnit(OpcodeUnitType.REGISTER, 0xA),
                                                                    OpcodeUnit(OpcodeUnitType.REGISTER, 0xC),
                                                                    OpcodeUnit(OpcodeUnitType.CONSTANT, 0xB)]

        yield of.parse_by_format(bytearray([0xAC, 0x1B]), 'XY1N'), [OpcodeUnit(OpcodeUnitType.REGISTER, 0xA),
                                                                    OpcodeUnit(OpcodeUnitType.REGISTER, 0xC),
                                                                    OpcodeUnit(OpcodeUnitType.CONSTANT, 0xB)]

        yield of.parse_by_format(bytearray([0xAC, 0x1B]), 'NNXN'), [OpcodeUnit(OpcodeUnitType.CONSTANT, 0xAC),
                                                                    OpcodeUnit(OpcodeUnitType.REGISTER, 0x1),
                                                                    OpcodeUnit(OpcodeUnitType.CONSTANT, 0xB)]

        yield of.parse_by_format(bytearray([0xAC, 0xAB]), 'NNAN'), [OpcodeUnit(OpcodeUnitType.CONSTANT, 0xAC),
                                                                    OpcodeUnit(OpcodeUnitType.CONSTANT, 0xB)]

        yield of.parse_by_format(bytearray([0x7C, 0xAB]), '7xNN'), [OpcodeUnit(OpcodeUnitType.REGISTER, 0xC),
                                                                    OpcodeUnit(OpcodeUnitType.CONSTANT, 0xAB)]

        yield of.parse_by_format(bytearray([0xAC, 0xAB]), 'XYXY'), [OpcodeUnit(OpcodeUnitType.REGISTER, 0xA),
                                                                    OpcodeUnit(OpcodeUnitType.REGISTER, 0xC),
                                                                    OpcodeUnit(OpcodeUnitType.REGISTER, 0xA),
                                                                    OpcodeUnit(OpcodeUnitType.REGISTER, 0xB)]

    def test_parse_by_format_should_return_right_units(self):
        for test in OpcodeFormatterTests._parse_by_format_tests():
            self.assertListEqual(test[1], test[0])
