#!/usr/bin/env python3


class Timer:
    def __init__(self, count: int =0):
        if not isinstance(count, int) or count < 0 or count > 255:
            raise ValueError('Timer count must be integer value in range [0;255]')
        self._count = count

    def decrease(self):
        if self._count != 0:
            self._count -= 1

    def get_count(self):
        return self._count

    def set_count(self, count: int):
        if not isinstance(count, int) or count < 0 or count > 255:
            raise ValueError('Timer count must be integer value in range [0;255]')
        self._count = count
