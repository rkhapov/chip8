#!/usr/bin/env python3


from abc import *


class Keyboard:
    @abstractmethod
    def update_state(self):
        raise NotImplemented

    @abstractmethod
    def is_key_pressed(self, key: str):
        raise NotImplemented

    @abstractmethod
    def is_key_available(self):
        raise NotImplemented

    @abstractmethod
    def get_pressed_key(self) -> str:
        raise NotImplemented
