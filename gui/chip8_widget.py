from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
from virtualmachine.timer import Timer
from virtualmachine.machine import Machine


class Chip8Widget(QWidget):

    pixel_width = 10
    pixel_height = 10

    def __init__(self, machine: Machine):
        super().__init__()
        self._machine = machine
        self.init_ui()

        self._draw_timer = Timer(count=255, interval=1.0 / 20)
        self._draw_timer.add_handler(self._draw_screen_event)
        self._draw_timer.start()

        self._machine_update_timer = Timer(count=255, interval=1.0 / 5000)
        self._machine_update_timer.add_handler(self._update_machine)
        self._machine_update_timer.start()

    def init_ui(self):
        self.setFixedSize(self._machine.Screen.width() * Chip8Widget.pixel_width,
                          self._machine.Screen.height() * Chip8Widget.pixel_height)
        self.setWindowTitle('Chip 8')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_screen(qp)
        qp.end()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_0:
            self._machine.Keyboard.key_down(0)
        elif event.key() == Qt.Key_1:
            self._machine.Keyboard.key_down(1)
        elif event.key() == Qt.Key_2:
            self._machine.Keyboard.key_down(2)
        elif event.key() == Qt.Key_3:
            self._machine.Keyboard.key_down(3)
        elif event.key() == Qt.Key_4:
            self._machine.Keyboard.key_down(4)
        elif event.key() == Qt.Key_5:
            self._machine.Keyboard.key_down(5)
        elif event.key() == Qt.Key_6:
            self._machine.Keyboard.key_down(6)
        elif event.key() == Qt.Key_7:
            self._machine.Keyboard.key_down(7)
        elif event.key() == Qt.Key_8:
            self._machine.Keyboard.key_down(8)
        elif event.key() == Qt.Key_9:
            self._machine.Keyboard.key_down(9)
        elif event.key() == Qt.Key_A:
            self._machine.Keyboard.key_down(0xA)
        elif event.key() == Qt.Key_B:
            self._machine.Keyboard.key_down(0xB)
        elif event.key() == Qt.Key_C:
            self._machine.Keyboard.key_down(0xC)
        elif event.key() == Qt.Key_D:
            self._machine.Keyboard.key_down(0xD)
        elif event.key() == Qt.Key_E:
            self._machine.Keyboard.key_down(0xE)
        elif event.key() == Qt.Key_F:
            self._machine.Keyboard.key_down(0xF)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_0:
            self._machine.Keyboard.key_up(0)
        elif event.key() == Qt.Key_1:
            self._machine.Keyboard.key_up(1)
        elif event.key() == Qt.Key_2:
            self._machine.Keyboard.key_up(2)
        elif event.key() == Qt.Key_3:
            self._machine.Keyboard.key_up(3)
        elif event.key() == Qt.Key_4:
            self._machine.Keyboard.key_up(4)
        elif event.key() == Qt.Key_5:
            self._machine.Keyboard.key_up(5)
        elif event.key() == Qt.Key_6:
            self._machine.Keyboard.key_up(6)
        elif event.key() == Qt.Key_7:
            self._machine.Keyboard.key_up(7)
        elif event.key() == Qt.Key_8:
            self._machine.Keyboard.key_up(8)
        elif event.key() == Qt.Key_9:
            self._machine.Keyboard.key_up(8)
        elif event.key() == Qt.Key_A:
            self._machine.Keyboard.key_up(0xA)
        elif event.key() == Qt.Key_B:
            self._machine.Keyboard.key_up(0xB)
        elif event.key() == Qt.Key_C:
            self._machine.Keyboard.key_up(0xC)
        elif event.key() == Qt.Key_D:
            self._machine.Keyboard.key_up(0xD)
        elif event.key() == Qt.Key_E:
            self._machine.Keyboard.key_up(0xE)
        elif event.key() == Qt.Key_F:
            self._machine.Keyboard.key_up(0xF)

    def _draw_screen_event(self):
        self._draw_timer.set_count(255)  # infinity loop
        self.update()

    def _update_machine(self):
        self._machine_update_timer.set_count(255)  # infinity loop
        self._machine.execute_next_instruction()

    def _draw_screen(self, qp):
        qp.setPen(QColor(0, 0, 0))
        for y in range(self._machine.Screen.height()):
            for x in range(self._machine.Screen.width()):
                self._draw_pixel(y, x, qp)

    def _draw_pixel(self, y, x, qp):
        qp.fillRect(x * Chip8Widget.pixel_width, y * Chip8Widget.pixel_height,
                    Chip8Widget.pixel_width, Chip8Widget.pixel_height,
                    QColor(0, 0, 0) if self._machine.Screen.get_pixel(y, x) == 0 else QColor(255, 255, 255))
