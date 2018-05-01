#!/usr/bin/env python3

from virtualmachine.instruction import *
from virtualmachine.machine import Machine


class Cls(Instruction):
    def execute(self, machine: Machine):
        machine.Screen.clear()

    @staticmethod
    def opcode_format() -> str:
        return '00E0'


class Rts(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

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
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '1NNN'


class Jsr(JumpInstruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '2NNN'


class Skeq(JumpInstruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '3XNN'


class Skne(JumpInstruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '4XNN'


class SkeqRegister(JumpInstruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '5XY0'


class MovConstantToRegister(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '6XNN'


class AddConstantToRegister(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '7XNN'


class MovRegisterToRegister(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy0'


class Or(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy1'


class And(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy2'


class Xor(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy3'


class AddRegisterToRegister(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy4'


class SubRegisterToRegister(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy5'


class Shr(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy6'


class Subn(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xy7'


class Shl(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '8xyE'


class SkneRegisters(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return '9xy0'


class Mvi(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'ANNN'


class Jmi(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'BNNN'


class Rand(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'CxNN'


class DrawSprite(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'DxyN'


class SkipIfKeyPressed(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Ex9E'


class SkipIfKeyNotPressed(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'ExA1'


class GetDelayTimer(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx07'


class WaitKey(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx0A'


class SetDelayTimer(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx15'


class SetSoundTimer(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx18'


class Adi(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx1E'


class LoadChar(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx29'


class Bcd(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx33'


class StoreRegisters(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx55'


class LoadRegisters(Instruction):
    def execute(self, machine: Machine):
        raise NotImplemented

    @staticmethod
    def opcode_format() -> str:
        return 'Fx65'
