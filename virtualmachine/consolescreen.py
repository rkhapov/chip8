#!/usr/bin/env python3

from virtualmachine.screen import Screen


class ConsoleScreen(Screen):
    def __init__(self, window, height=32, width=64):
        super().__init__()
        self._init_screen(height, width)
        self._window = window

    def _init_screen(self, height, width):
        self._screen = []
        self._height = height
        self._width = width
        for i in range(self._height):
            self._screen.append([0] * self._width)

    def height(self):
        return self._height

    def width(self):
        return self._width

    def curses_window(self):
        return self._window

    def set_pixel(self, y, x, value):
        if value != 0 and value != 1:
            raise ValueError('Pixel value should be 1 or 0')
        y = y % self._height
        x = x % self._width
        self._screen[y][x] = value

    def get_pixel(self, y, x):
        y = y % self._height
        x = x % self._width
        return self._screen[y][x]

    def clear(self):
        for y in range(self._height):
            for x in range(self._width):
                self._screen[y][x] = 0

    def update(self):
        self._window.clear()
        self._draw_screen()
        self._window.refresh()

    def _draw_screen(self):
        for y in range(0, self._height):
            for x in range(0, self._width):
                self._draw_pixel(y, x)

    def _draw_pixel(self, y, x):
        self._window.addch(y, x, '#' if self._screen[y][x] == 1 else ' ')
