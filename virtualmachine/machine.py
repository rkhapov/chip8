#!/usr/bin/env python3

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


class Keyboard:
    def __init__(self):
        self._keys = [0] * 16

    def key_down(self, key: int):
        self._keys[key] = True

    def key_up(self, key: int):
        self._keys[key] = False

    def is_key_pressed(self, key: int):
        return self._keys[key]

    def get_first_pressed(self):
        for key in range(16):
            if self._keys[key]:
                return key
        return None

    def is_any_key_pressed(self):
        for key in self._keys:
            if key:
                return True
        return False


class Screen:
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
        if value != 0 and value != 1:
            raise ValueError('Pixel value should be 1 or 0')
        y = y % self._height
        x = x % self._width

        old_value = self._screen[y][x]
        new_value = self._screen[y][x] ^ value
        self._screen[y][x] = new_value

        return old_value == 1 and new_value == 0  # return 1 if collision

    def get_pixel(self, y, x):
        y = y % self._height
        x = x % self._width
        return self._screen[y][x]

    def clear(self):
        for y in range(self._height):
            for x in range(self._width):
                self._screen[y][x] = 0


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
        self.DelayTimer = Timer()
        self.SoundTimer = Timer()
        self.SoundTimer.add_handler(self.make_sound)
        self.DelayTimer.start()
        self.SoundTimer.start()
        self.Block = False

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

    def make_sound(self):
        pass

    def execute_next_instruction(self):
        if self._instruction_executing:
            return

        if self._end_program_reached():
            self.ExitCode = 0
            return

        self._instruction_executing = True

        instruction = self._get_next_instruction()
        instruction.execute(self)

        # print(instruction.__class__.__name__, instruction.arg_constant, instruction.arg_registers)

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
