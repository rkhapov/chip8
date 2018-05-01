#!/usr/bin/env python3


from virtualmachine.screen import Screen
from virtualmachine.keyboard import Keyboard
from virtualmachine.timer import Timer


class Stack:
    def __init__(self):
        self._stack = []

    def pop(self):
        if self.size() == 0:
            raise RuntimeError('Pop from empty stack')

        ret = self.top()
        self._stack.pop()
        return ret

    def push(self, value):
        self._stack.append(value)

    def size(self):
        return len(self._stack)

    def top(self):
        if self.size() == 0:
            raise RuntimeError('top from empty stack')

        return self._stack[self.size() - 1]


class Machine:
    def __init__(self, screen: Screen, keyboard: Keyboard, memory_size: int = 0x1000):
        self.Screen = screen
        self.Keyboard = keyboard
        self.Stack = Stack()
        self.Memory = Machine.create_memory(memory_size)
        self.MemorySize = len(self.Memory)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None
        self.DelayTimer = Timer()
        self.SoundTimer = Timer()
        self.SoundTimer.add_handler(self.make_sound)
        self.DelayTimer.start()
        self.SoundTimer.start()

    def reset(self):
        self.Screen.clear()
        self.Stack = Stack()
        self.Memory = Machine.create_memory(self.MemorySize)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None
        self.DelayTimer.set_count(0)
        self.SoundTimer.set_count(0)

    def make_sound(self):
        pass

    @staticmethod
    def create_memory(memory_size):
        memory = bytearray(memory_size)

        standard_sprite = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
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

        for i in range(len(standard_sprite)):
            memory[i] = standard_sprite[i]

        return memory
