#!/usr/bin/env python3


from virtualmachine.machine import Machine


class Interpreter:
    def __init__(self, machine: Machine):
        self._machine = machine
        self._program = bytearray()

    def run_program(self):
        raise NotImplemented

    def load_program(self, filename):
        with open(filename, 'rb') as file:
            self._program = file.read()
