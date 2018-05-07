import unittest
from parser.instruction_factory import InstructionFactory
from virtualmachine.instructions import *


class InstructionFactoryTests(unittest.TestCase):

    def setUp(self):
        self.factory = InstructionFactory()

    @staticmethod
    def _from_opcode_tests_cases():
        yield bytearray([0x00, 0xE0]), Cls, None, [], 'cls'
        yield bytearray([0x00, 0xEE]), Rts, None, [], 'rts'
        yield bytearray([0x10, 0xFF]), Jmp, 0x0FF, [], 'jmp1'
        yield bytearray([0x12, 0xFF]), Jmp, 0x2FF, [], 'jmp2'
        yield bytearray([0x12, 0xB1]), Jmp, 0x2B1, [], 'jmp3'
        yield bytearray([0x22, 0xB1]), Jsr, 0x2B1, [], 'jsr1'
        yield bytearray([0x22, 0xFF]), Jsr, 0x2FF, [], 'jsr2'
        yield bytearray([0x32, 0xFF]), Skeq, 0xFF, [2], 'skeq'
        yield bytearray([0x4B, 0xCC]), Skne, 0xCC, [0xB], 'skne'
        yield bytearray([0x5B, 0xC0]), SkeqRegister, None, [0xB, 0xC], 'skeq registers'
        yield bytearray([0x62, 0xAA]), MovConstantToRegister, 0xAA, [0x2], 'mov constant to register'
        yield bytearray([0x7E, 0xBC]), AddConstantToRegister, 0xBC, [0xE], 'add constant to register'
        yield bytearray([0x8E, 0xB0]), MovRegisterToRegister, None, [0xE, 0xB], 'mov register to register'
        yield bytearray([0x8E, 0xB1]), Or, None, [0xE, 0xB], 'or'
        yield bytearray([0x8E, 0xB2]), And, None, [0xE, 0xB], 'and'
        yield bytearray([0x81, 0xC3]), Xor, None, [0x1, 0xC], 'xor'
        yield bytearray([0x81, 0xC4]), AddRegisterToRegister, None, [0x1, 0xC], 'add register to register'
        yield bytearray([0x81, 0xC5]), SubRegisterToRegister, None, [0x1, 0xC], 'sub register to register'
        yield bytearray([0x81, 0xC6]), Shr, None, [0x1, 0xC], 'shr'
        yield bytearray([0x81, 0xC7]), Subn, None, [0x1, 0xC], 'subn'
        yield bytearray([0x92, 0x30]), SkneRegisters, None, [0x2, 0x3], 'skne registers'
        yield bytearray([0xAF, 0x30]), Mvi, 0xF30, [], 'mvi'
        yield bytearray([0xBF, 0x30]), Jmi, 0xF30, [], 'jmi'
        yield bytearray([0xCA, 0x44]), Rand, 0x44, [0xA], 'rand'
        yield bytearray([0xDA, 0x44]), DrawSprite, 0x4, [0xA, 0x4], 'draw'
        yield bytearray([0xEA, 0x9E]), SkipIfKeyPressed, None, [0xA], 'skip if key pressed'
        yield bytearray([0xEA, 0xA1]), SkipIfKeyNotPressed, None, [0xA], 'skip if not key pressed'
        yield bytearray([0xFA, 0x07]), GetDelayTimer, None, [0xA], 'get delay'
        yield bytearray([0xFB, 0x0A]), WaitKey, None, [0xB], 'wait key'
        yield bytearray([0xFB, 0x15]), SetDelayTimer, None, [0xB], 'set delay'
        yield bytearray([0xFB, 0x18]), SetSoundTimer, None, [0xB], 'set sound'
        yield bytearray([0xFB, 0x1E]), Adi, None, [0xB], 'adi'
        yield bytearray([0xFC, 0x29]), LoadChar, None, [0xC], 'load char'
        yield bytearray([0xFC, 0x33]), Bcd, None, [0xC], 'bcd'
        yield bytearray([0xFC, 0x55]), StoreRegisters, None, [0xC], 'store registers'
        yield bytearray([0xFC, 0x65]), LoadRegisters, None, [0xC], 'load registers'

    def test_create_from_opcode_should_return_right_instruction(self):
        for test in InstructionFactoryTests._from_opcode_tests_cases():
            sut = self.factory.from_opcode(test[0])

            self.assertTrue(isinstance(sut, test[1]), msg=test[4] + ' isinstance')
            self.assertEqual(sut.arg_constant, test[2], msg=test[4] + ' arg_constant')
            self.assertListEqual(sut.arg_registers, test[3], msg=test[4] + ' arg_registers')
