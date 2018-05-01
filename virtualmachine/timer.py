#!/usr/bin/env python3

import threading
import time


class Timer:
    def __init__(self, count=0, interval=1.0 / 60):
        self._tick = []
        self._interval = interval
        self._count = count
        self._thread = threading.Thread(target=self._tick_event, daemon=True)

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()

    def add_handler(self, handler):
        self._tick.append(handler)

    def _tick_event(self):
        while True:
            time.sleep(self._interval)

            if self._count > 0:
                for tick in self._tick:
                    tick()
                self._count -= 1

    def set_count(self, count):
        if not isinstance(count, int) or count < 0 or count > 255:
            raise TypeError('Count of timer must be integer in range[0;255]')
        self._count = count

    def get_count(self):
        return self._count


