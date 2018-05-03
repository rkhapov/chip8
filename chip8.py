#!/usr/bin/env python3

import sys
from gui.chip8_widget import *


def main():
    if len(sys.argv) < 2:
        print('Expected program filename')
        return 1

    machine = Machine()
    machine.load_program(sys.argv[1])

    app = QApplication(sys.argv)
    chip8 = Chip8Widget(machine)
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
