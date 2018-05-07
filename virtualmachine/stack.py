#!/usr/bin/env python3


class Stack:
    def __init__(self):
        self._stack = []

    def pop(self):
        if self.size() == 0:
            raise RuntimeError('Pop from empty stack')

        return self._stack.pop()

    def push(self, value):
        self._stack.append(value)

    def size(self):
        return len(self._stack)

    def top(self):
        if self.size() == 0:
            raise RuntimeError('top from empty stack')

        return self._stack[self.size() - 1]
