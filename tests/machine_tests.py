import unittest
from virtualmachine.instructions import *


class MachineTests(unittest.TestCase):

    @staticmethod
    def _load_char_tests_cases():
        yield 0x0, [0xf0, 0x90, 0x90, 0x90, 0xf0], '0'
        yield 0x1, [0x20, 0x60, 0x20, 0x20, 0x70], '1'
        yield 0x2, [0xf0, 0x10, 0xf0, 0x80, 0xf0], '2'
        yield 0x3, [0xf0, 0x10, 0xf0, 0x10, 0xf0], '3'
        yield 0x4, [0x90, 0x90, 0xf0, 0x10, 0x10], '4'
        yield 0x5, [0xf0, 0x80, 0xf0, 0x10, 0xf0], '5'
        yield 0x6, [0xf0, 0x80, 0xf0, 0x90, 0xf0], '6'
        yield 0x7, [0xf0, 0x10, 0x20, 0x40, 0x40], '7'
        yield 0x8, [0xf0, 0x90, 0xf0, 0x90, 0xf0], '8'
        yield 0x9, [0xf0, 0x90, 0xf0, 0x10, 0xf0], '9'
        yield 0xA, [0xf0, 0x90, 0xf0, 0x90, 0x90], '10'
        yield 0xB, [0xe0, 0x90, 0xe0, 0x90, 0xe0], '11'
        yield 0xC, [0xf0, 0x80, 0x80, 0x80, 0xf0], '12'
        yield 0xD, [0xe0, 0x90, 0x90, 0x90, 0xe0], '13'
        yield 0xE, [0xf0, 0x80, 0xf0, 0x80, 0xf0], '14'
        yield 0xF, [0xf0, 0x80, 0xf0, 0x80, 0x80], '15'

    def test_font_addresses_should_point_in_right_sprites(self):
        machine = Machine()

        for digit in MachineTests._load_char_tests_cases():
            for k in range(5):
                self.assertEqual(machine.Memory[machine.FontDict[digit[0]] + k], digit[1][k], msg=digit[2])

    def test_execute_next_instruction_increase_pc_by_two_if_instruction_are_not_jump(self):
        machine = Machine()
        machine.PC = 100
        machine.Memory[100] = 0x00  # Cls instruction
        machine.Memory[101] = 0xE0

        machine.execute_next_instruction()

        self.assertEqual(machine.PC, 102)

    def test_execute_next_instruction_doesnt_change_pc_after_jump_instruction(self):
        machine = Machine()
        machine.PC = 100
        machine.Memory[100] = 0x1E  # Jump at 0xEAB
        machine.Memory[101] = 0xAB

        machine.execute_next_instruction()

        self.assertEqual(machine.PC, 0xEAB)

    def test_after_block_doesnt_change_pc(self):
        machine = Machine()
        machine.PC = 100
        machine.Memory[100] = 0xF5  # WaitKey at V5
        machine.Memory[101] = 0x0A

        machine.execute_next_instruction()

        self.assertTrue(machine.Block)
        self.assertEqual(machine.PC, 100)
