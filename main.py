from PIL import ImageQt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from tomatofont import to_tomato_image
import datetime
import signal
import sys
import itertools

app = QtWidgets.QApplication([])
NUM_MINUTES = int(sys.argv[1])

def make_tomato_icon(minutes):
    time_remaining_img = to_tomato_image(minutes)
    qimage = ImageQt.ImageQt(time_remaining_img)
    qpixmap = QtGui.QPixmap.fromImage(qimage)
    return QtGui.QIcon(qpixmap)


# we need this to make it so ^c will quit the program
signal.signal(signal.SIGINT, signal.SIG_DFL)


def change_icon():
    tray.setIcon(blank_icon)
    timer_icon = make_tomato_icon(tomato_timer.minutes_remaining)
    QTimer.singleShot(100, lambda: tray.setIcon(timer_icon))

timer = QTimer()
timer.timeout.connect(change_icon)
timer.start(1000)


class TomatoTimer:

    def __init__(self):
        self._td = datetime.timedelta(minutes=NUM_MINUTES)
        self._timer = None

    @property
    def minutes_remaining(self):
        return int(self._td.total_seconds() / 60)

    @property
    def is_running(self):
        return self._timer and self._timer.isActive()

    def start(self):
        self.stop_timer()

        self._timer = QTimer()
        self._timer.timeout.connect(self._decr_timer)
        self._timer.start(1000)

    def stop_timer(self):
        if self._timer:
            self._timer.stop()

    def _decr_timer(self):
        if self._td == datetime.timedelta(0):
            self.stop_timer()
        self._td -= datetime.timedelta(seconds=1)


tomato_timer = TomatoTimer()
tomato_timer.start()


blank_pixmap = QtGui.QPixmap(1, 1)
blank_pixmap.fill(Qt.transparent)
blank_icon = QtGui.QIcon(blank_pixmap)

w = QtWidgets.QWidget()
tray = QtWidgets.QSystemTrayIcon(make_tomato_icon(tomato_timer.minutes_remaining), w)
tray.show()

sys.exit(app.exec_())
