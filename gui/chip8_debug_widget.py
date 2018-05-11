
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from gui.chip8_machine_state_widget import Chip8MachineStateWidget
from gui.chip8_screen_widget import Chip8ScreenWidget
from tools.timer import Timer
from virtualmachine.machine import Machine


class Chip8DebugWidget(QWidget):

    def __init__(self, machine: Machine):
        super().__init__()
        self._machine = machine
        self.init_ui()
        self._sound = QSound('beep.wav')

        self._executed_number = 0

        self._key_dict = {
            Qt.Key_1: 1, Qt.Key_2: 2, Qt.Key_3: 3, Qt.Key_4: 0xC,
            Qt.Key_Q: 4, Qt.Key_W: 5, Qt.Key_E: 6, Qt.Key_R: 0xD,
            Qt.Key_A: 7, Qt.Key_S: 8, Qt.Key_D: 9, Qt.Key_F: 0xE,
            Qt.Key_Z: 0xA, Qt.Key_X: 0x0, Qt.Key_C: 0xB, Qt.Key_V: 0xF
        }

    def init_ui(self):
        screen = Chip8ScreenWidget(self._machine.Screen, self)
        state = Chip8MachineStateWidget(self._machine, self)
        layout = QHBoxLayout()
        layout.addWidget(screen)
        layout.addWidget(state)
        self.setLayout(layout)
        self.setWindowTitle('Chip 8')
        self.show()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() in self._key_dict:
            self._machine.Keyboard.key_down(self._key_dict[event.key()])

        if event.key() == Qt.Key_Space:
            print('execute')
            self._execute_instruction()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.key() in self._key_dict:
            self._machine.Keyboard.key_up(self._key_dict[event.key()])

    def _execute_instruction(self):
        print('execute')
        self._machine.execute_next_instruction()
        self._update_sound_delay()
        self._executed_number += 1

    def _update_sound_delay(self):
        if self._executed_number % 10 != 0:
            return

        if self._machine.SoundTimer.get_count() != 0:
            self._sound.play()
        self._machine.DelayTimer.decrease()
        self._machine.SoundTimer.decrease()
