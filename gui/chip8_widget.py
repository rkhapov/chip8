
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QWidget

from gui.chip8_screen_widget import Chip8ScreenWidget
from tools.timer import Timer
from virtualmachine.machine import Machine


class Chip8Widget(QWidget):

    def __init__(self, machine: Machine, sound: bool=False, instruction_per_second: int = 500):
        super().__init__()
        self._machine = machine
        self.init_ui()
        self._sound = QSound('beep.wav')
        self._sound_support = sound

        self._machine_update_timer = Timer(interval=1.0 / instruction_per_second)
        self._machine_update_timer.add_handler(self._execute_instruction)
        self._machine_update_timer.start()

        self._machine_sound_delay_timer = Timer(interval=1.0 / 60)  # 60 Hz
        self._machine_sound_delay_timer.add_handler(self._update_sound_delay)
        self._machine_sound_delay_timer.start()

        self._key_dict = {
            Qt.Key_1: 1, Qt.Key_2: 2, Qt.Key_3: 3, Qt.Key_4: 0xC,
            Qt.Key_Q: 4, Qt.Key_W: 5, Qt.Key_E: 6, Qt.Key_R: 0xD,
            Qt.Key_A: 7, Qt.Key_S: 8, Qt.Key_D: 9, Qt.Key_F: 0xE,
            Qt.Key_Z: 0xA, Qt.Key_X: 0x0, Qt.Key_C: 0xB, Qt.Key_V: 0xF
        }

    def init_ui(self):
        screen = Chip8ScreenWidget(self._machine.Screen, self)
        self.setWindowTitle('Chip 8')
        self.show()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() in self._key_dict:
            self._machine.Keyboard.key_down(self._key_dict[event.key()])

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.key() in self._key_dict:
            self._machine.Keyboard.key_up(self._key_dict[event.key()])

    def _execute_instruction(self):
        self._machine.execute_next_instruction()

    def _update_sound_delay(self):
        if self._machine.SoundTimer.get_count() != 0 and self._sound_support:
            self._sound.play()
        self._machine.DelayTimer.decrease()
        self._machine.SoundTimer.decrease()
