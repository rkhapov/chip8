import sys
import argparse

from PyQt5.QtWidgets import QApplication

from gui.chip8_debug_widget import Chip8DebugWidget
from gui.chip8_widget import Chip8Widget
from virtualmachine.machine import Machine


class RunConfiguration:
    def __init__(self, filename: str, debug: bool, sound: bool, compatibility: bool, instructions_per_second):
        self._filename = filename
        self._debug = debug
        self._sound = sound
        self._compatibility = compatibility
        self._instructions_per_second = instructions_per_second

    def run(self):
        machine = Machine(compatibility_load_store=self._compatibility)
        machine.load_program(self._filename)

        app = QApplication(sys.argv)

        if not self._debug:
            chip8 = Chip8Widget(machine, self._sound, self._instructions_per_second)
        else:
            chip8 = Chip8DebugWidget(machine, self._sound)

        chip8.show()
        return app.exec_()

    @staticmethod
    def from_args():

        desc = '''
This is the CHIP-8 interpreter
It usages PyQt5, so you should install it

Keyboard:
CHIP-8 keyboard    real keyboard 
+---------------+  +---------------+  
| 1 | 2 | 3 | C |  | 1 | 2 | 3 | 4 |
+---------------+  +---------------+
| 4 | 5 | 6 | D |  | Q | W | E | R |
+---------------+  +---------------+
| 7 | 8 | 9 | E |  | A | S | D | F |
+---------------+  +---------------+
| A | 0 | B | F |  | Z | X | C | V |
+---------------+  +---------------+
Space usages as execute next instruction in debug mode

Written by rkhapov (r.khapov@yandex.ru)
'''

        parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('filename', help='file with chip8 program')
        parser.add_argument('-s', '--sound', help='enable sound for chip8', action="store_true")
        parser.add_argument('-d', '--debug', help='enable debug mode', action="store_true")
        parser.add_argument('-c', '--compatibility', help='enable compatibility mode for store and load instructions',
                            action='store_true')
        parser.add_argument('-f', '--frequency', help='frequency: amount of executing instructions per second',
                            type=int, default=500)
        args = parser.parse_args()

        filename = args.filename

        return RunConfiguration(filename, args.debug, args.sound, args.compatibility, args.frequency)
