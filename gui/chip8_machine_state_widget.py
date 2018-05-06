from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel

from tools.timer import Timer
from virtualmachine.machine import Machine


class Chip8MachineStateWidget(QWidget):

    def __init__(self, machine: Machine):
        super().__init__()
        self._machine = machine
        screen_size = QDesktopWidget().screenGeometry(-1)
        self._pixel_width = int(screen_size.width() * 1 / 100)
        self._pixel_height = self._pixel_width

        self._label = QLabel()
        self._label.setParent(self)
        self.show()

        self._draw_timer = Timer(count=255, interval=1.0 / 60)
        self._draw_timer.add_handler(self._draw_state_event)
        self._draw_timer.start()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_state(qp)
        qp.end()

    def _draw_state_event(self):
        self._draw_timer.set_count(255)  # infinity loop
        self.update()

    def _draw_state(self, qp):
        self._label.setText('VRegisters: {}\n'
                            'PC: {}\n'
                            'AddressRegister: {}'
                            .format(list(map(int, self._machine.VRegisters)),
                                    self._machine.PC,
                                    self._machine.AddressRegister))
