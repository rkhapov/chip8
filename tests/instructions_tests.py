import unittest
from virtualmachine.instructions import *
from virtualmachine.machine import Machine


class InstructionTests(unittest.TestCase):
    def test_cls_instruction_clears_screen(self):
        machine = Machine()
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
        machine = Machine()
        machine.Stack.push(15)
        machine.Stack.push(16)

        rts = Rts()

        rts.execute(machine)

        self.assertTrue(isinstance(rts, JumpInstruction))
        self.assertEqual(machine.Stack.size(), 1)
        self.assertEqual(machine.Stack.top(), 15)
        self.assertEqual(machine.PC, 16)

    def test_jmp_should_change_pc_for_parameter(self):
        machine = Machine()

        jmp = Jmp()
        jmp.arg_constant = 0x250

        jmp.execute(machine)

        self.assertTrue(isinstance(jmp, JumpInstruction))
        self.assertEqual(machine.PC, 0x250)

    def test_jsr_should_call_subroutine(self):
        machine = Machine()
        machine.PC = 10

        jsr = Jsr()
        jsr.arg_constant = 0xEEF

        jsr.execute(machine)

        self.assertTrue(isinstance(jsr, JumpInstruction))
        self.assertEqual(machine.PC, 0xEEF)
        self.assertEqual(machine.Stack.top(), 12)

    def test_skeq_should_skip_if_equals(self):
        machine = Machine()
        machine.PC = 10
        machine.VRegisters[2] = 0xEE

        skeq = Skeq()
        skeq.arg_constant = 0xEE
        skeq.arg_registers.append(2)
        skeq.execute(machine)

        self.assertTrue(isinstance(skeq, JumpInstruction))
        self.assertEqual(machine.PC, 14)

    def test_skeq_should_not_skip_if_not_equals(self):
        machine = Machine()
        machine.PC = 10
        machine.VRegisters[2] = 0xAC

        skeq = Skeq()
        skeq.arg_constant = 0xEE
        skeq.arg_registers.append(2)
        skeq.execute(machine)

        self.assertTrue(isinstance(skeq, JumpInstruction))
        self.assertEqual(machine.PC, 12)

    def test_skne_should_skip_if_not_equals(self):
        machine = Machine()
        machine.PC = 10
        machine.VRegisters[2] = 0xBC

        skne = Skne()
        skne.arg_constant = 0xEE
        skne.arg_registers.append(2)
        skne.execute(machine)

        self.assertTrue(isinstance(skne, JumpInstruction))
        self.assertEqual(machine.PC, 14)

    def test_skne_should_not_skip_if_equals(self):
        machine = Machine()
        machine.PC = 10
        machine.VRegisters[2] = 0xEE

        skne = Skne()
        skne.arg_constant = 0xEE
        skne.arg_registers.append(2)
        skne.execute(machine)

        self.assertTrue(isinstance(skne, JumpInstruction))
        self.assertEqual(machine.PC, 12)

    def test_skeq_registers_should_skip_if_equals(self):
        machine = Machine()
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
        machine = Machine()
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
        machine = Machine()
        machine.VRegisters[0xA] = 15

        mov = MovConstantToRegister()
        mov.arg_registers.append(0xA)
        mov.arg_constant = 0xAC

        mov.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xAC)

    def test_add_constant_to_register_should_change_value_right(self):
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA

        add = AddConstantToRegister()
        add.arg_registers.append(0xA)
        add.arg_constant = 0x3

        add.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xFA + 3)

    def test_add_constant_to_register_should_change_value_right_with_overflow(self):
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA

        add = AddConstantToRegister()
        add.arg_registers.append(0xA)
        add.arg_constant = 0xAC

        add.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xFA + 0xAC) % 0x100)
        self.assertEqual(machine.VRegisters[0xF], 0)

    def test_mov_register_to_register(self):
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        mov = MovRegisterToRegister()
        mov.arg_registers.append(0xA)
        mov.arg_registers.append(0xB)

        mov.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_or(self):
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        ori = Or()
        ori.arg_registers.append(0xA)
        ori.arg_registers.append(0xB)

        ori.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE | 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_and(self):
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        andi = And()
        andi.arg_registers.append(0xA)
        andi.arg_registers.append(0xB)

        andi.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE & 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_xor(self):
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xEE

        xor = Xor()
        xor.arg_registers.append(0xA)
        xor.arg_registers.append(0xB)

        xor.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xEE ^ 0xFA)
        self.assertEqual(machine.VRegisters[0xB], 0xEE)

    def test_add_register_to_register_shouldnt_set_vf_if_carry_if_sum_less_256(self):
        machine = Machine()
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
        machine = Machine()
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
        machine = Machine()
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
        machine = Machine()
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
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xFF

        shr = Shr()
        shr.arg_registers.append(0xA)
        shr.arg_registers.append(0xB)

        shr.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], 0xFA >> 1)
        self.assertEqual(machine.VRegisters[0xB], 0xFF)
        self.assertEqual(machine.VRegisters[0xF], 0)

    def test_subn_should_set_vf_if_vy_greater_vx(self):
        machine = Machine()
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
        machine = Machine()
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
        machine = Machine()
        machine.VRegisters[0xA] = 0xFA
        machine.VRegisters[0xB] = 0xFF

        shl = Shl()
        shl.arg_registers.append(0xA)
        shl.arg_registers.append(0xB)

        shl.execute(machine)

        self.assertEqual(machine.VRegisters[0xA], (0xFA << 1) % 0x100)
        self.assertEqual(machine.VRegisters[0xB], 0xFF)
        self.assertEqual(machine.VRegisters[0xF], 1)

    def test_skne_registers_should_skip_if_not_equal(self):
        machine = Machine()
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
        machine = Machine()
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
        machine = Machine()

        mvi = Mvi()
        mvi.arg_constant = 0xABC

        mvi.execute(machine)

        self.assertEqual(machine.AddressRegister, 0xABC)

    def test_jmi_should_change_PC_right(self):
        machine = Machine()
        machine.VRegisters[0] = 0xAB

        jmi = Jmi()
        jmi.arg_constant = 0x111

        jmi.execute(machine)

        self.assertEqual(machine.PC, 0xAB + 0x111)
        self.assertTrue(isinstance(jmi, JumpInstruction))

    def test_load_char_should_set_right_address(self):
        machine = Machine()

        load = LoadChar()
        load.arg_registers.append(0x5)

        for digit in range(16):
            machine.VRegisters[5] = digit
            load.execute(machine)

            self.assertEqual(machine.AddressRegister, machine.FontDict[digit])

    def test_skip_if_key_pressed_should_skip_if_key_flag_is_equal_to_1_anyway_nobody_reads_it(self):
        machine = Machine()
        machine.Keyboard.key_down(4)
        machine.VRegisters[5] = 4

        skip = SkipIfKeyPressed()
        skip.arg_registers.append(5)

        skip.execute(machine)

        self.assertEqual(machine.PC, 4)

    def test_skip_if_key_pressed_should_not_skip_if_key_flag_is_equal_to_0(self):
        machine = Machine()
        machine.Keyboard.key_down(7)
        machine.VRegisters[5] = 4

        skip = SkipIfKeyPressed()
        skip.arg_registers.append(5)

        skip.execute(machine)

        self.assertEqual(machine.PC, 2)

    def test_skip_if_not_pressed_should_not_skip_if_key_pressed(self):
        machine = Machine()
        machine.Keyboard.key_down(3)
        machine.VRegisters[8] = 3

        skip = SkipIfKeyNotPressed()
        skip.arg_registers.append(8)

        skip.execute(machine)

        self.assertEqual(machine.PC, 2)

    def test_skip_if_not_pressed_should_skip_if_key_not_pressed(self):
        machine = Machine()
        machine.Keyboard.key_down(8)
        machine.VRegisters[8] = 3

        skip = SkipIfKeyNotPressed()
        skip.arg_registers.append(8)

        skip.execute(machine)

        self.assertEqual(machine.PC, 4)

    def test_wait_key_blocks_machine(self):
        machine = Machine()

        wait = WaitKey()
        wait.execute(machine)

        self.assertTrue(machine.Block)

    def test_wait_key_unblock_when_key_pressed_and_return_right_key(self):
        machine = Machine()

        wait = WaitKey()
        wait.arg_registers.append(4)
        wait.execute(machine)

        machine.Keyboard.key_down(5)

        wait.execute(machine)

        self.assertEqual(machine.VRegisters[4], 5)
        self.assertFalse(machine.Block)

    def test_bcd_should_get_right_digits(self):
        machine = Machine()
        machine.VRegisters[7] = 107

        bcd = Bcd()
        bcd.arg_registers.append(7)

        bcd.execute(machine)

        self.assertEqual(machine.Memory[machine.AddressRegister], machine.FontDict[1])
        self.assertEqual(machine.Memory[machine.AddressRegister + 1], machine.FontDict[0])
        self.assertEqual(machine.Memory[machine.AddressRegister + 2], machine.FontDict[7])

    def test_store_registers_should_store_and_increase_address_register(self):
        machine = Machine()
        for i in range(6):
            machine.VRegisters[i] = i
        machine.AddressRegister = 123

        store = StoreRegisters()
        store.arg_registers.append(5)

        store.execute(machine)

        for i in range(6):
            self.assertEqual(machine.Memory[123 + i], machine.VRegisters[i])
        self.assertEqual(machine.AddressRegister, 123 + 5 + 1)

    def test_load_registers_should_load_registers_and_increase_address_register(self):
        machine = Machine()
        for i in range(6):
            machine.Memory[123 + i] = i
        machine.AddressRegister = 123

        load = LoadRegisters()
        load.arg_registers.append(5)

        load.execute(machine)

        for i in range(6):
            self.assertEqual(machine.VRegisters[i], machine.Memory[123 + i])
        self.assertEqual(machine.AddressRegister, 123 + 5 + 1)
