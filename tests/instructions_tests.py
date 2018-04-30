import unittest
from virtualmachine.screen import Screen
from instructions.cls_instruction import ClsInstruction
from virtualmachine.machine import Machine


class TestScreen(Screen):
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
        pass


class InstructionTests(unittest.TestCase):
    def test_cls_instruction_clears_screen(self):
        machine = Machine(TestScreen())
        cls = ClsInstruction()

        machine.Screen.set_pixel(5, 5, 1)
        machine.Screen.set_pixel(4, 8, 1)
        machine.Screen.set_pixel(10, 10, 1)
        machine.Screen.set_pixel(2, 15, 1)
        machine.Screen.set_pixel(0, 0, 1)
        machine.Screen.set_pixel(22, 34, 1)
        machine.Screen.set_pixel(22, 63, 1)

        cls.execute(machine)

        for i in range(machine.Screen.height()):
            for j in range(machine.Screen.width()):
                self.assertEqual(machine.Screen.get_pixel(i, j), 0)
