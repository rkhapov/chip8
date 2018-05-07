#!/usr/bin/env python3


class Keyboard:
    def __init__(self):
        self._keys = [0] * 16

    def key_down(self, key: int):
        self._keys[key] = True

    def key_up(self, key: int):
        self._keys[key] = False

    def is_key_pressed(self, key: int):
        return self._keys[key]

    def get_first_pressed(self):
        for key in range(16):
            if self._keys[key]:
                return key
        return None

    def is_any_key_pressed(self):
        for key in self._keys:
            if key:
                return True
        return False
