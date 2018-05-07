#!/usr/bin/env python3

import threading
import time


class Timer:
    def __init__(self, interval=1.0 / 60):
        self._tick = []
        self._interval = interval
        self._thread = threading.Thread(target=self._tick_event, daemon=True)

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()

    def add_handler(self, handler):
        self._tick.append(handler)

    def _tick_event(self):
        while True:
            time.sleep(self._interval)

            for tick in self._tick:
                tick()

    def set_interval(self, interval):
        self._interval = interval

    def get_interval(self):
        return self._interval
