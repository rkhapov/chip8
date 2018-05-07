#!/usr/bin/env python3


class Screen:
    def __init__(self, height=32, width=64):
        self._screen = []
        self._height = height
        self._width = width
        for i in range(self._height):
            self._screen.append([0] * self._width)

    def height(self):
        return self._height

    def width(self):
        return self._width

    def set_pixel(self, y, x, value):
        if value != 0 and value != 1:
            raise ValueError('Pixel value should be 1 or 0')
        y = y % self._height
        x = x % self._width

        self._screen[y][x] ^= value

        return value == 1 and self._screen[y][x] == 0  # return 1 if collision

    def get_pixel(self, y, x):
        y = y % self._height
        x = x % self._width
        return self._screen[y][x]

    def clear(self):
        for y in range(self._height):
            for x in range(self._width):
                self._screen[y][x] = 0
