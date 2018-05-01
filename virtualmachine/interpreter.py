#!/usr/bin/env python3


from virtualmachine.machine import Machine
from parser.instruction_factory import InstructionFactory
from virtualmachine.screen import Screen
from virtualmachine.instruction import JumpInstruction


class Interpreter:
    def __init__(self, screen: Screen):
        self._machine = Machine(screen)
        self._instruction_factory = InstructionFactory()

    def run_program(self):
        while self._machine.ExitCode is None:
            self._execute_next_instruction()

        return self._machine.ExitCode

    def load_program_bytes(self, program: bytearray):
        self._machine.reset()
        for i in range(len(program)):
            self._machine.Memory[i] = program[i]

    def load_program(self, filename):
        with open(filename, 'rb') as file:
            self.load_program_bytes(bytearray(file.read()))

    def _execute_next_instruction(self):
        opcode = self._read_next_instruction()
        instruction = self._instruction_factory.from_opcode(opcode)
        instruction.execute(self._machine)

        if not isinstance(instruction, JumpInstruction):
            self._machine.PC += 2

    def _read_next_instruction(self):
        return bytearray([self._machine.Memory[self._machine.PC], self._machine.Memory[self._machine.PC + 1]])
