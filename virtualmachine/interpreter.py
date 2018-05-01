#!/usr/bin/env python3
import logging
import time

from parser.instruction_factory import InstructionFactory
from virtualmachine.instruction import JumpInstruction
from virtualmachine.keyboard import Keyboard
from virtualmachine.machine import Machine
from virtualmachine.screen import Screen


class Interpreter:
    def __init__(self, screen: Screen, keyboard: Keyboard):
        self._machine = Machine(screen, keyboard)
        self._instruction_factory = InstructionFactory()

    def run_program(self):
        self._machine.PC = 0x200
        while self._machine.ExitCode is None:
            self._execute_next_instruction()
            time.sleep(0.005)

        return self._machine.ExitCode

    def load_program_bytes(self, program: bytearray):
        self._machine.reset()
        for i in range(len(program)):
            self._machine.Memory[0x200 + i] = program[i]

    def load_program(self, filename):
        with open(filename, 'rb') as file:
            program = bytearray(file.read())
            self.load_program_bytes(program)

    def _execute_next_instruction(self):
        opcode = self._read_next_instruction()

        if opcode == bytearray([0, 0]):
            self._machine.ExitCode = 0
            return
        instruction = self._instruction_factory.from_opcode(opcode)

        # logging.info('executing: {} '.format(instruction.__class__.__name__) +
        #              'with arguments: {} {}'.format(instruction.arg_constant, instruction.arg_registers) +
        #              ' registers: {}'.format(list(self._machine.VRegisters)))

        instruction.execute(self._machine)

        if not isinstance(instruction, JumpInstruction):
            self._machine.PC += 2

    def _read_next_instruction(self):
        return bytearray([self._machine.Memory[self._machine.PC], self._machine.Memory[self._machine.PC + 1]])
