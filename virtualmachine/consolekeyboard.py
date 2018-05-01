#!/ust/bin/env python3

import curses
from virtualmachine.keyboard import Keyboard
from virtualmachine.consolescreen import ConsoleScreen


class ConsoleKeyboard(Keyboard):
    def __init__(self, screen: ConsoleScreen):
        self._window = screen.curses_window()
        self._window.keypad(True)
        self._window.nodelay(True)
        curses.nocbreak()
        curses.noecho()

        self._pressed_key = ''

    def update_state(self):
        self._pressed_key = self._getch().lower()

    def is_key_pressed(self, key: str):
        return self._pressed_key == key.lower()

    def is_key_available(self):
        return self._pressed_key != ''

    def get_pressed_key(self) -> str:
        return self._pressed_key

    def _getch(self):
        try:
            return str(self._window.getkey())
        except:  # no key pressed
            return ''
