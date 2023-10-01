from PyQt6.QtWidgets import QApplication

from yauza.gui.widgets import MainWindow
from yauza.train import Yauza


class App(QApplication):
    def __init__(self, w, h, *args, **kwargs):
        QApplication.__init__(self, *args, **kwargs)
        yauza = Yauza()
        window = MainWindow(yauza)
        window.resize(w, h)
        window.show()
        self.window = window

    def exec(self):
        print("application started")
        res = QApplication.exec()
        print("bye")
        return res
