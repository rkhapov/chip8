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
    def __init__(self, screen: Screen, keyboard: Keyboard, memory_size: int=0x1000):
        self.Screen = screen
        self.Keyboard = keyboard
        self.Stack = Stack()
        self.Memory = bytearray(memory_size)
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
        self.Memory = bytearray(self.MemorySize)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None
        self.DelayTimer.set_count(0)
        self.SoundTimer.set_count(0)

    def make_sound(self):
        pass
