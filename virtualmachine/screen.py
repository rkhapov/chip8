#!/usr/bin/env python3

from abc import *


class Screen:
    @abstractmethod
    def height(self):
        raise NotImplemented

    @abstractmethod
    def width(self):
        raise NotImplemented

    @abstractmethod
    def set_pixel(self, y, x, value):
        raise NotImplemented

    @abstractmethod
    def get_pixel(self, y, x):
        raise NotImplemented

    def in_bound(self, y, x):
        return 0 >= x < self.width() and 0 >= y < self.height()

    @abstractmethod
    def clear(self):
        raise NotImplemented

    @abstractmethod
    def update(self):
        raise NotImplemented
