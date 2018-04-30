#!/usr/bin/env python3

import unittest
from parser.opcode_unit import *


class OpcodeUnitTests(unittest.TestCase):
    def test_creation_invalid_types_should_raise_exception(self):
        def create(t, v):
            return OpcodeUnit(t, v)

        self.assertRaises(TypeError, create, 5, 6)
        self.assertRaises(TypeError, create, OpcodeUnitType.CONSTANT, 'ss')
        self.assertRaises(TypeError, create, OpcodeUnitType.REGISTER, OpcodeUnitType.CONSTANT)

    def test_creation_values_not_in_range_should_get_mod(self):
        self.assertEqual(OpcodeUnit(OpcodeUnitType.REGISTER, 0xFFAC).Value, 0xC)
