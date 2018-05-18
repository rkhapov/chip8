from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel

from tools.timer import Timer
from virtualmachine.machine import Machine
from parser.instruction_factory import *


def to_hex(i: int) -> str:
    return hex(i)[2:].upper().zfill(2)


class Chip8MachineStateWidget(QWidget):
    def __init__(self, machine: Machine, parent: QWidget=None):
        super().__init__(parent)
        self._machine = machine

        self._init_ui()

        self._draw_timer = Timer(interval=1.0 / 30)
        self._draw_timer.add_handler(self._draw_state_event)
        self._draw_timer.start()

        self._instruction_factory = InstructionFactory()

    def _init_ui(self):
        screen_size = QDesktopWidget().screenGeometry(-1)
        self._pixel_width = int(screen_size.width() * 1 / 100)
        self._pixel_height = self._pixel_width

        self.setFixedHeight(self._pixel_height * 32)
        self.setFixedWidth(self._pixel_width * 35)

        self._text_size = int(self._pixel_height * 0.7)

        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self._draw_state(qp)

        qp.end()

    def _draw_state_event(self):
        self.update()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        self.parent().keyPressEvent(a0)

    def _draw_state(self, qp):
        qp.setFont(QFont('Noto Sans', self._text_size))

        t = self._text_size // 2

        qp.drawText(0, self._text_size, 'V: {}'.format(list(map(to_hex, self._machine.VRegisters))))
        qp.drawText(0, 2 * self._text_size + t, 'PC: {}, I: {}, DT: {}, ST: {}'
                    .format(to_hex(self._machine.PC),
                            to_hex(self._machine.AddressRegister),
                            to_hex(self._machine.DelayTimer.get_count()),
                            to_hex(self._machine.SoundTimer.get_count())))
        qp.drawText(0, 3 * self._text_size + 2 * t, 'Stack: {}'.format(list(map(to_hex, self._machine.Stack.items()))))
        qp.drawText(0, 4 * self._text_size + 3 * t, 'Memory at 10-radius of PC:')

        y = 5 * self._text_size + 4 * t

        for i in range(-10, 11):
            index = self._machine.PC + i * 2

            if index < 0 or index > self._machine.MemorySize:
                qp.drawText(0, y, '')
                continue

            opcode = self._get_opcode_at(index)

            try:
                instruction = self._instruction_factory.from_opcode(opcode)

                qp.drawText(0, y, '{}{} : {}, {} {} {}'
                            .format('-> ' if i == 0 else '    ',
                                    to_hex(index),
                                    list(map(to_hex, opcode)),
                                    instruction.__class__.__name__,
                                    list((map(to_hex, instruction.arg_registers))),
                                    to_hex(instruction.arg_constant) if instruction.arg_constant is not None else '-'))
            except InstructionFactoryError:
                qp.drawText(0, y, '{}{} : {}, [unknown]'
                            .format('-> ' if i == 0 else '    ',
                                    to_hex(index),
                                    list(map(to_hex, opcode))))

            y += self._text_size + t

        qp.drawText(0, y, 'Machine blocked' if self._machine.Block else 'Machine not blocked')

    def _get_opcode_at(self, i):
        return bytearray([self._machine.Memory[i], self._machine.Memory[i + 1]])
