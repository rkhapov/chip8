
from PyQt5 import QtGui
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from tools.timer import Timer
from virtualmachine.machine import Machine


class Chip8Widget(QWidget):

    pixel_width = 10
    pixel_height = 10

    def __init__(self, machine: Machine):
        super().__init__()
        self._machine = machine
        self.init_ui()
        self._sound = QSound('beep.wav')

        self._draw_timer = Timer(count=255, interval=1.0 / 20)
        self._draw_timer.add_handler(self._draw_screen_event)
        self._draw_timer.start()

        self._machine_update_timer = Timer(count=255, interval=1.0 / 7000)
        self._machine_update_timer.add_handler(self._update_machine)
        self._machine_update_timer.start()

        self._key_dict = {
            Qt.Key_1: 1, Qt.Key_2: 2, Qt.Key_3: 3, Qt.Key_4: 0xC,
            Qt.Key_Q: 4, Qt.Key_W: 5, Qt.Key_E: 6, Qt.Key_R: 0xD,
            Qt.Key_A: 7, Qt.Key_S: 8, Qt.Key_D: 9, Qt.Key_F: 0xE,
            Qt.Key_Z: 0xA, Qt.Key_X: 0x0, Qt.Key_C: 0xB, Qt.Key_V: 0xF
        }

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
        if event.key() in self._key_dict:
            self._machine.Keyboard.key_down(self._key_dict[event.key()])

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.key() in self._key_dict:
            self._machine.Keyboard.key_up(self._key_dict[event.key()])

    def _draw_screen_event(self):
        self._draw_timer.set_count(255)  # infinity loop
        self.update()

    def _update_machine(self):
        self._machine_update_timer.set_count(255)  # infinity loop
        if self._machine.SoundTimer.get_count() != 0:
            self._play_sound()
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

    def _play_sound(self):
        self._sound.play()
