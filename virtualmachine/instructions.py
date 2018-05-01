#!/usr/bin/env python3
import logging

from virtualmachine.instruction import *
from virtualmachine.machine import Machine
from random import randint


class Cls(Instruction):
    def execute(self, machine: Machine):
        machine.Screen.clear()
        machine.Screen.update()

    @staticmethod
    def opcode_format() -> str:
        return '00E0'


class Rts(JumpInstruction):
    def execute(self, machine: Machine):
        machine.PC = machine.Stack.pop()

    @staticmethod
    def opcode_format() -> str:
        return '00EE'


class Scdown(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '00CN'


class Scright(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '00FB'


class Scleft(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '00FC'


class Low(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '00FE'


class High(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '00FF'


class Jmp(JumpInstruction):
    def execute(self, machine: Machine):
        machine.PC = self.arg_constant

    @staticmethod
    def opcode_format() -> str:
        return '1NNN'


class Jsr(JumpInstruction):
    def execute(self, machine: Machine):
        machine.Stack.push(machine.PC + 2)
        machine.PC = self.arg_constant

    @staticmethod
    def opcode_format() -> str:
        return '2NNN'


class Skeq(JumpInstruction):
    def execute(self, machine: Machine):
        if machine.VRegisters[self.arg_registers[0]] == self.arg_constant:
            machine.PC += 4
        else:
            machine.PC += 2

    @staticmethod
    def opcode_format() -> str:
        return '3XNN'


class Skne(JumpInstruction):
    def execute(self, machine: Machine):
        if machine.VRegisters[self.arg_registers[0]] != self.arg_constant:
            machine.PC += 4
        else:
            machine.PC += 2

    @staticmethod
    def opcode_format() -> str:
        return '4XNN'


class SkeqRegister(JumpInstruction):
    def execute(self, machine: Machine):
        if machine.VRegisters[self.arg_registers[0]] == machine.VRegisters[self.arg_registers[1]]:
            machine.PC += 4
        else:
            machine.PC += 2

    @staticmethod
    def opcode_format() -> str:
        return '5XY0'


class MovConstantToRegister(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = self.arg_constant

    @staticmethod
    def opcode_format() -> str:
        return '6XNN'


class AddConstantToRegister(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = (self.arg_constant
                                                     + machine.VRegisters[self.arg_registers[0]]) % 0x100

    @staticmethod
    def opcode_format() -> str:
        return '7XNN'


class MovRegisterToRegister(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = machine.VRegisters[self.arg_registers[1]]

    @staticmethod
    def opcode_format() -> str:
        return '8xy0'


class Or(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = machine.VRegisters[self.arg_registers[0]] | \
                                                    machine.VRegisters[self.arg_registers[1]]

    @staticmethod
    def opcode_format() -> str:
        return '8xy1'


class And(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = machine.VRegisters[self.arg_registers[0]] & \
                                                    machine.VRegisters[self.arg_registers[1]]

    @staticmethod
    def opcode_format() -> str:
        return '8xy2'


class Xor(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = machine.VRegisters[self.arg_registers[0]] ^ \
                                                    machine.VRegisters[self.arg_registers[1]]

    @staticmethod
    def opcode_format() -> str:
        return '8xy3'


class AddRegisterToRegister(Instruction):
    def execute(self, machine: Machine):
        add = machine.VRegisters[self.arg_registers[0]] + machine.VRegisters[self.arg_registers[1]]
        machine.VRegisters[0xF] = 0 if add < 0x100 else 1
        machine.VRegisters[self.arg_registers[0]] = add % 0x100

    @staticmethod
    def opcode_format() -> str:
        return '8xy4'


class SubRegisterToRegister(Instruction):
    def execute(self, machine: Machine):
        sub = machine.VRegisters[self.arg_registers[0]] - machine.VRegisters[self.arg_registers[1]]
        machine.VRegisters[0xF] = 0 if sub < 0 else 1
        machine.VRegisters[self.arg_registers[0]] = sub % 0x100

    @staticmethod
    def opcode_format() -> str:
        return '8xy5'


class Shr(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = machine.VRegisters[self.arg_registers[1]] >> 1
        machine.VRegisters[0xF] = machine.VRegisters[self.arg_registers[1]] % 2

    @staticmethod
    def opcode_format() -> str:
        return '8xy6'


class Subn(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[0xF] = 1 if machine.VRegisters[self.arg_registers[1]] \
                                       > machine.VRegisters[self.arg_registers[0]] else 0
        machine.VRegisters[self.arg_registers[0]] = (machine.VRegisters[self.arg_registers[1]] -
                                                     machine.VRegisters[self.arg_registers[0]]) % 0x100

    @staticmethod
    def opcode_format() -> str:
        return '8xy7'


class Shl(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = (machine.VRegisters[self.arg_registers[1]] << 1) % 0x100
        machine.VRegisters[0xF] = machine.VRegisters[self.arg_registers[1]] & 0X80 != 0

    @staticmethod
    def opcode_format() -> str:
        return '8xyE'


class SkneRegisters(JumpInstruction):
    def execute(self, machine: Machine):
        if machine.VRegisters[self.arg_registers[0]] == machine.VRegisters[self.arg_registers[1]]:
            machine.PC += 2
        else:
            machine.PC += 4

    @staticmethod
    def opcode_format() -> str:
        return '9xy0'


class Mvi(Instruction):
    def execute(self, machine: Machine):
        machine.AddressRegister = self.arg_constant

    @staticmethod
    def opcode_format() -> str:
        return 'ANNN'


class Jmi(JumpInstruction):
    def execute(self, machine: Machine):
        machine.PC = machine.VRegisters[0] + self.arg_constant

    @staticmethod
    def opcode_format() -> str:
        return 'BNNN'


class Rand(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = randint(0, 255) & self.arg_constant

    @staticmethod
    def opcode_format() -> str:
        return 'CxNN'


class DrawSprite(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[0xF] = 0
        y = machine.VRegisters[self.arg_registers[1]]
        x = machine.VRegisters[self.arg_registers[0]]

        for i in range(self.arg_constant):
            img = machine.Memory[machine.AddressRegister + i]

            for k in range(8):
                pixel = (img & (1 << (7 - k))) >> (7 - k)
                old_pixel = machine.Screen.get_pixel(y + i, x + k)
                new_pixel = pixel ^ old_pixel

                if old_pixel == 1 and new_pixel == 0:
                    machine.VRegisters[0xF] = 1

                machine.Screen.set_pixel(y + i, x + k, new_pixel)

        machine.Screen.update()

    @staticmethod
    def opcode_format() -> str:
        return 'DxyN'


class SkipIfKeyPressed(JumpInstruction):
    def execute(self, machine: Machine):
        machine.Keyboard.update_state()
        key = hex(machine.VRegisters[self.arg_registers[0]])[2:]
        if machine.Keyboard.is_key_pressed(key):
            machine.PC += 4
        else:
            machine.PC += 2

    @staticmethod
    def opcode_format() -> str:
        return 'Ex9E'


class SkipIfKeyNotPressed(JumpInstruction):
    def execute(self, machine: Machine):
        machine.Keyboard.update_state()
        key = hex(machine.VRegisters[self.arg_registers[0]])[2:]
        if not machine.Keyboard.is_key_pressed(key):
            machine.PC += 4
        else:
            machine.PC += 2

    @staticmethod
    def opcode_format() -> str:
        return 'ExA1'


class GetDelayTimer(Instruction):
    def execute(self, machine: Machine):
        machine.VRegisters[self.arg_registers[0]] = machine.DelayTimer.get_count()

    @staticmethod
    def opcode_format() -> str:
        return 'Fx07'


class WaitKey(Instruction):
    def execute(self, machine: Machine):
        while not machine.Keyboard.is_key_available():
            machine.Keyboard.update_state()
        machine.VRegisters[self.arg_registers[0]] = int(machine.Keyboard.get_pressed_key(), 16)

    @staticmethod
    def opcode_format() -> str:
        return 'Fx0A'


class SetDelayTimer(Instruction):
    def execute(self, machine: Machine):
        machine.DelayTimer.set_count(machine.VRegisters[self.arg_registers[0]])

    @staticmethod
    def opcode_format() -> str:
        return 'Fx15'


class SetSoundTimer(Instruction):
    def execute(self, machine: Machine):
        machine.SoundTimer.set_count(machine.VRegisters[self.arg_registers[0]])

    @staticmethod
    def opcode_format() -> str:
        return 'Fx18'


class Adi(Instruction):
    def execute(self, machine: Machine):
        machine.AddressRegister += machine.VRegisters[self.arg_registers[0]]

    @staticmethod
    def opcode_format() -> str:
        return 'Fx1E'


class LoadChar(Instruction):
    def execute(self, machine: Machine):
        machine.AddressRegister = 5 * machine.VRegisters[self.arg_registers[0]]

    @staticmethod
    def opcode_format() -> str:
        return 'Fx29'


class Bcd(Instruction):
    def execute(self, machine: Machine):
        hundreds = machine.Memory[self.arg_registers[0]] // 100
        tens = (machine.Memory[self.arg_registers[0]] // 10) % 10
        ones = machine.Memory[self.arg_registers[0]] % 10

        machine.Memory[machine.AddressRegister] = 5 * hundreds
        machine.Memory[machine.AddressRegister + 1] = 5 * tens
        machine.Memory[machine.AddressRegister + 2] = 5 * ones

    @staticmethod
    def opcode_format() -> str:
        return 'Fx33'


class StoreRegisters(Instruction):
    def execute(self, machine: Machine):
        for i in range(0, self.arg_registers[0] + 1):
            machine.Memory[machine.AddressRegister + i] = machine.VRegisters[i]

    @staticmethod
    def opcode_format() -> str:
        return 'Fx55'


class LoadRegisters(Instruction):
    def execute(self, machine: Machine):
        for i in range(0, self.arg_registers[0] + 1):
            machine.VRegisters[i] = machine.Memory[machine.AddressRegister + i]

    @staticmethod
    def opcode_format() -> str:
        return 'Fx65'
