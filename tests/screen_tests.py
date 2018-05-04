#!/usr/bin/env python3


import unittest
from virtualmachine.machine import Screen


class ScreenTests(unittest.TestCase):
    def test_clear_should_set_all_pixels_to_zero(self):
        screen = Screen()
        screen.set_pixel(10, 3, 1)
        screen.set_pixel(3, 13, 1)
        screen.set_pixel(30, 15, 1)
        screen.set_pixel(30, 31, 1)
        screen.set_pixel(30, 25, 1)

        screen.clear()

        for i in range(screen.height()):
            for j in range(screen.width()):
                self.assertEqual(screen.get_pixel(i, j), 0)

    def test_set_pixel_should_change_value_right(self):
        screen = Screen()
        screen.set_pixel(5, 5, 1)

        self.assertEqual(screen.get_pixel(5, 5), 1)

        screen.set_pixel(5, 5, 0)

        self.assertEqual(screen.get_pixel(5, 5), 1)

        screen.set_pixel(5, 5, 1)

        self.assertEqual(screen.get_pixel(5, 5), 0, msg='Expected collision')

    def test_set_pixel_should_return_0_if_no_collision(self):
        screen = Screen()
        screen.set_pixel(5, 5, 1)

        self.assertEqual(screen.set_pixel(6, 6, 1), 0)
        self.assertEqual(screen.set_pixel(5, 5, 0), 0)

    def test_set_pixel_should_return_1_if_collision(self):
        screen = Screen()
        screen.set_pixel(5, 5, 1)

        self.assertEqual(screen.set_pixel(5, 5, 1), 1)

    def test_set_pixel_should_take_cords_by_module(self):
        screen = Screen()
        screen.set_pixel(55, 55, 1)

        self.assertEqual(screen.get_pixel(55 % 64, 55 % 32), 1)
