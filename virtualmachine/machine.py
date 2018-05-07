#!/usr/bin/env python3

from virtualmachine.timer import Timer
from virtualmachine.stack import Stack
from virtualmachine.keyboard import Keyboard
from virtualmachine.screen import Screen


class Machine:
    def __init__(self, memory_size: int = 0x1000):
        self.Screen = Screen()
        self.Keyboard = Keyboard()
        self.MemorySize = memory_size
        self.Stack = Stack()
        self.Memory = Machine.create_memory(self.MemorySize)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None
        self.DelayTimer = Timer(0)
        self.SoundTimer = Timer(0)
        self.Block = False
        self.FontDict = Machine._create_font_dict()

        import parser.instruction_factory
        self._instruction_factory = parser.instruction_factory.InstructionFactory()
        self._instruction_executing = False

    def reset(self):
        self.Screen.clear()
        self.Stack = Stack()
        self.Keyboard = Keyboard()
        self.Memory = Machine.create_memory(self.MemorySize)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None
        self.DelayTimer.set_count(0)
        self.SoundTimer.set_count(0)

    def execute_next_instruction(self):
        if self._instruction_executing:
            return

        if self._end_program_reached():
            self.ExitCode = 0
            return

        self._instruction_executing = True

        instruction = self._get_next_instruction()
        instruction.execute(self)

        from virtualmachine.instruction import JumpInstruction
        if not isinstance(instruction, JumpInstruction) and not self.Block:
            self.PC += 2

        self._instruction_executing = False

    def load_program(self, program, start_address: int = 0x200):
        if not isinstance(program, bytearray):
            with open(program, 'rb') as program_file:
                program = program_file.read()

        for i in range(len(program)):
            self.Memory[i + start_address] = program[i]
        self.PC = start_address

    def _get_next_instruction(self):
        opcode = self._get_next_instruction_opcode()

        return self._instruction_factory.from_opcode(opcode)

    def _get_next_instruction_opcode(self):
        return bytearray([self.Memory[self.PC], self.Memory[self.PC + 1]])

    def _end_program_reached(self):
        return self.ExitCode is not None or self.PC >= self.MemorySize \
               or self._get_next_instruction_opcode() == bytearray([0, 0])

    _standard_sprites = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                         0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                         0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                         0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                         0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
                         0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                         0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                         0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                         0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                         0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                         0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                         0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                         0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                         0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                         0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                         0xF0, 0x80, 0xF0, 0x80, 0x80]  # F

    @staticmethod
    def create_memory(memory_size):
        memory = bytearray(memory_size)

        for i in range(len(Machine._standard_sprites)):
            memory[i] = Machine._standard_sprites[i]

        return memory

    @staticmethod
    def _create_font_dict():
        font = {}

        for i in range(16):
            font[i] = i * 5

        return font
