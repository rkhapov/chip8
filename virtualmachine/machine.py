#!/usr/bin/env python3


from virtualmachine.screen import Screen


class Machine:
    def __init__(self, screen: Screen, memory_size: int=0x1000):
        self.Screen = screen
        self.Stack = []
        self.Memory = bytearray(memory_size)
        self.MemorySize = len(self.Memory)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None

    def reset(self):
        self.Screen.clear()
        self.Stack = []
        self.Memory = bytearray(self.MemorySize)
        self.PC = 0
        self.VRegisters = bytearray(16)
        self.AddressRegister = 0
        self.ExitCode = None
