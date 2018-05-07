from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel

from tools.timer import Timer
from virtualmachine.machine import Machine


def to_hex(i: int) -> str:
    return hex(i)[2:].upper().zfill(2)


class Chip8MachineStateWidget(QWidget):

    def __init__(self, machine: Machine):
        super().__init__()
        self._machine = machine

        self._init_ui()

        self._draw_timer = Timer(interval=1.0 / 60)
        self._draw_timer.add_handler(self._draw_state_event)
        self._draw_timer.start()

    def _init_ui(self):
        screen_size = QDesktopWidget().screenGeometry(-1)
        self._pixel_width = int(screen_size.width() * 1 / 100)
        self._pixel_height = self._pixel_width

        self.setFixedHeight(self._pixel_height * 75)
        self.setFixedWidth(self._pixel_width * 45)

        self._text_size = int(self._pixel_height * 0.85)

        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self._draw_state(qp)

        qp.end()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        self._machine.execute_next_instruction()

    def _draw_state_event(self):
        self.update()

    def _draw_state(self, qp):
        qp.setFont(QFont('Noto Sans', self._text_size))

        qp.drawText(0, self._text_size, 'V: {}'.format(list(map(to_hex, self._machine.VRegisters))))
        qp.drawText(0, 2 * self._text_size + 5, 'PC: {}, I: {}, DT: {}, ST: {}'
                    .format(to_hex(self._machine.PC),
                            to_hex(self._machine.AddressRegister),
                            to_hex(self._machine.DelayTimer.get_count()),
                            to_hex(self._machine.SoundTimer.get_count())))
        qp.drawText(0, 3 * self._text_size + 10, 'Stack: {}'.format(list(map(to_hex, self._machine.Stack.items()))))
