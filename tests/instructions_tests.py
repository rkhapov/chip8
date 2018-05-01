import unittest
from virtualmachine.screen import Screen
from virtualmachine.instructions import *
from virtualmachine.machine import Machine


class TestScreen(Screen):
    def __init__(self, height=32, width=64):
        self._screen = []
        self._height = height
        self._width = width
        for i in range(self._height):
            self._screen.append([0] * self._width)

    def height(self):
        return self._height

    def width(self):
        return self._width

    def set_pixel(self, y, x, value):
        y = y % self._height
        x = x % self._width
        self._screen[y][x] = value

    def get_pixel(self, y, x):
        y = y % self._height
        x = x % self._width
        return self._screen[y][x]

    def clear(self):
        for y in range(self._height):
            for x in range(self._width):
                self._screen[y][x] = 0

    def update(self):
        pass


class InstructionTests(unittest.TestCase):
    def test_cls_instruction_clears_screen(self):
        machine = Machine(TestScreen(), None)
        cls = Cls()

        machine.Screen.set_pixel(5, 5, 1)
        machine.Screen.set_pixel(4, 8, 1)
        machine.Screen.set_pixel(10, 10, 1)
        machine.Screen.set_pixel(2, 15, 1)
        machine.Screen.set_pixel(0, 0, 1)
        machine.Screen.set_pixel(22, 34, 1)
        machine.Screen.set_pixel(22, 63, 1)

        cls.execute(machine)

        for i in range(machine.Screen.height()):
            for j in range(machine.Screen.width()):
                self.assertEqual(machine.Screen.get_pixel(i, j), 0)

    def test_rts_should_set_up_pc_at_stack_top(self):
        machine = Machine(None, None)
        machine.Stack.push(15)
        machine.Stack.push(16)

        rts = Rts()

        rts.execute(machine)

        self.assertTrue(isinstance(rts, JumpInstruction))
        self.assertEqual(machine.Stack.size(), 1)
        self.assertEqual(machine.Stack.top(), 15)
        self.assertEqual(machine.PC, 16)

    def test_jmp_should_change_pc_for_parameter(self):
        machine = Machine(None, None)

        jmp = Jmp()
        jmp.arg_constant = 0x250

        jmp.execute(machine)

        self.assertTrue(isinstance(jmp, JumpInstruction))
        self.assertEqual(machine.PC, 0x250)

    def test_jsr_should_call_subroutine(self):
        machine = Machine(None, None)
        machine.PC = 10

        jsr = Jsr()
        jsr.arg_constant = 0xEEF

        jsr.execute(machine)

        self.assertTrue(isinstance(jsr, JumpInstruction))
        self.assertEqual(machine.PC, 0xEEF)
        self.assertEqual(machine.Stack.top(), 12)

    def test_skeq_should_skip_if_equals(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[2] = 0xEE

        skeq = Skeq()
        skeq.arg_constant = 0xEE
        skeq.arg_registers.append(2)
        skeq.execute(machine)

        self.assertTrue(isinstance(skeq, JumpInstruction))
        self.assertEqual(machine.PC, 14)

    def test_skeq_should_not_skip_if_not_equals(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[2] = 0xAC

        skeq = Skeq()
        skeq.arg_constant = 0xEE
        skeq.arg_registers.append(2)
        skeq.execute(machine)

        self.assertTrue(isinstance(skeq, JumpInstruction))
        self.assertEqual(machine.PC, 12)

    def test_skne_should_skip_if_not_equals(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[2] = 0xBC

        skne = Skne()
        skne.arg_constant = 0xEE
        skne.arg_registers.append(2)
        skne.execute(machine)

        self.assertTrue(isinstance(skne, JumpInstruction))
        self.assertEqual(machine.PC, 14)

    def test_skne_should_not_skip_if_equals(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[2] = 0xEE

        skne = Skne()
        skne.arg_constant = 0xEE
        skne.arg_registers.append(2)
        skne.execute(machine)

        self.assertTrue(isinstance(skne, JumpInstruction))
        self.assertEqual(machine.PC, 12)

    def test_skeq_registers_should_skip_if_equals(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[2] = 0xEE
        machine.VRegisters[5] = 0xEE

        skeq = SkeqRegister()
        skeq.arg_registers.append(2)
        skeq.arg_registers.append(5)
        skeq.execute(machine)

        self.assertTrue(isinstance(skeq, JumpInstruction))
        self.assertEqual(machine.PC, 14)

    def test_skeq_registers_should_not_skip_if_not_equals(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[2] = 0xEE
        machine.VRegisters[5] = 0xE4

        skeq = SkeqRegister()
        skeq.arg_registers.append(2)
        skeq.arg_registers.append(5)
        skeq.execute(machine)

        self.assertTrue(isinstance(skeq, JumpInstruction))
        self.assertEqual(machine.PC, 12)

    def test_mov_constant_to_register_should_change_target_register(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 15

        mov = MovConstantToRegister()
        mov.arg_registers.append(0xA)
        mov.arg_constant = 0xAC

        mov.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xAC)

    def test_add_constant_to_register_should_change_value_right(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA

        add = AddConstantToRegister()
        add.arg_registers.append(0xA)
        add.arg_constant = 0x3

        add.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xFA + 3)

    def test_add_constant_to_register_should_change_value_right_with_overflow(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA

        add = AddConstantToRegister()
        add.arg_registers.append(0xA)
        add.arg_constant = 0xAC

        add.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xFA + 0xAC) % 0x100)
        self.assertEqual(machine.VRegisters[0xF], 0)

    def test_mov_register_to_register(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        mov = MovRegisterToRegister()
        mov.arg_registers.append(0xA)
        mov.arg_registers.append(0xB)

        mov.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_or(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        ori = Or()
        ori.arg_registers.append(0xA)
        ori.arg_registers.append(0xB)

        ori.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE | 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_and(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        andi = And()
        andi.arg_registers.append(0xA)
        andi.arg_registers.append(0xB)

        andi.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE & 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_xor(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        xor = Xor()
        xor.arg_registers.append(0xA)
        xor.arg_registers.append(0xB)

        xor.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE ^ 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_add_register_to_register_shouldnt_set_vf_if_carry_if_sum_less_256(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0x1

        add = AddRegisterToRegister()
        add.arg_registers.append(0xA)
        add.arg_registers.append(0xB)

        add.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0x1 + 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0x1)
        self.assertEqual(machine.VRegisters[0xF], 0)

    def test_add_register_to_register_should_set_vf_if_carry_if_sum_greater_256(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        add = AddRegisterToRegister()
        add.arg_registers.append(0xA)
        add.arg_registers.append(0xB)

        add.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xEE + 0xFA) % 0x100)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)
        self.assertEqual(machine.VRegisters[0xF], 1)

    def test_sub_register_to_register_should_set_vf_if_sub_are_positive(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0x1

        sub = SubRegisterToRegister()
        sub.arg_registers.append(0xA)
        sub.arg_registers.append(0xB)

        sub.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xFA - 0x1)
        self.assertEqual(machine.VRegisters[0xB], 0x1)
        self.assertEqual(machine.VRegisters[0xF], 1)

    def test_add_register_to_register_shouldnt_set_vf_if_sub_are_negative(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xFF

        sub = SubRegisterToRegister()
        sub.arg_registers.append(0xA)
        sub.arg_registers.append(0xB)

        sub.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xFA - 0xFF) % 0x100)
        self.assertEqual(machine.VRegisters[0xB], 0xFF)
        self.assertEqual(machine.VRegisters[0xF], 0)

    def test_shr_should_write_least_significant_bit_at_vf(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xFF

        shr = Shr()
        shr.arg_registers.append(0xA)
        shr.arg_registers.append(0xB)

        shr.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xFF >> 1)
        self.assertEqual(machine.VRegisters[0xB], 0xFF)
        self.assertEqual(machine.VRegisters[0xF], 1)

    def test_subn_should_set_vf_if_vy_greater_vx(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xFF

        subn = Subn()
        subn.arg_registers.append(0xA)
        subn.arg_registers.append(0xB)

        subn.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xFF - 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xFF)
        self.assertEqual(machine.VRegisters[0xF], 1)

    def test_subn_should_set_vf_to_0_if_vy_less_vx(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFF
        machine.VRegisters[0xB] = 0xFA

        subn = Subn()
        subn.arg_registers.append(0xA)
        subn.arg_registers.append(0xB)

        subn.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xFA - 0xFF) % 0x100)
        self.assertEqual(machine.VRegisters[0xB], 0xFA)
        self.assertEqual(machine.VRegisters[0xF], 0)

    def test_shr_should_write_most_significant_bit_at_vf(self):
        machine = Machine(None, None)
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xFF

        shl = Shl()
        shl.arg_registers.append(0xA)
        shl.arg_registers.append(0xB)

        shl.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xFF << 1) % 0x100)
        self.assertEqual(machine.VRegisters[0xB], 0xFF)
        self.assertEqual(machine.VRegisters[0xF], 1)

    def test_skne_registers_should_skip_if_not_equal(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[1] = 5
        machine.VRegisters[2] = 6

        skne = SkneRegisters()
        skne.arg_registers.append(1)
        skne.arg_registers.append(2)

        skne.execute(machine)

        self.assertTrue(isinstance(skne, JumpInstruction))
        self.assertEqual(machine.PC, 14)

    def test_skne_registers_shouldnt_skip_if_equal(self):
        machine = Machine(None, None)
        machine.PC = 10
        machine.VRegisters[1] = 5
        machine.VRegisters[2] = 5

        skne = SkneRegisters()
        skne.arg_registers.append(1)
        skne.arg_registers.append(2)

        skne.execute(machine)

        self.assertTrue(isinstance(skne, JumpInstruction))
        self.assertEqual(machine.PC, 12)

    def test_mvi_should_change_address_register(self):
        machine = Machine(None, None)

        mvi = Mvi()
        mvi.arg_constant = 0xABC

        mvi.execute(machine)

        self.assertEqual(machine.AddressRegister, 0xABC)

    def test_jmi_should_change_PC_right(self):
        machine = Machine(None, None)
        machine.VRegisters[0] = 0xAB

        jmi = Jmi()
        jmi.arg_constant = 0x111

        jmi.execute(machine)

        self.assertEqual(machine.PC, 0xAB + 0x111)
        self.assertTrue(isinstance(jmi, JumpInstruction))




