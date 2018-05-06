from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from tools.timer import Timer
from virtualmachine.machine import Screen


class Chip8ScreenWidget(QWidget):

    def __init__(self, screen: Screen):
        super().__init__()
        self._screen = screen
        screen_size = QDesktopWidget().screenGeometry(-1)
        self._pixel_width = int(screen_size.width() * 1 / 100)
        self._pixel_height = self._pixel_width

        self.init_ui()

        self._draw_timer = Timer(count=255, interval=1.0 / 60)
        self._draw_timer.add_handler(self._draw_screen_event)
        self._draw_timer.start()

    def init_ui(self):
        self.setFixedSize(self._screen.width() * self._pixel_width,
                          self._screen.height() * self._pixel_height)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._draw_screen(qp)
        qp.end()

    def _draw_screen_event(self):
        self._draw_timer.set_count(255)  # infinity loop
        self.update()

    def _draw_screen(self, qp):
        qp.setPen(QColor(0, 0, 0))
        for y in range(self._screen.height()):
            for x in range(self._screen.width()):
                self._draw_pixel(y, x, qp)

    def _draw_pixel(self, y, x, qp):
        qp.fillRect(x * self._pixel_width, y * self._pixel_height,
                    self._pixel_width, self._pixel_height,
                    QColor(0, 0, 0) if self._screen.get_pixel(y, x) == 0 else QColor(255, 255, 255))
