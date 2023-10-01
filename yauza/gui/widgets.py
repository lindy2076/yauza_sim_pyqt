from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import pyqtSignal, QTimer

from yauza.train import Yauza


class KVRVButton(QPushButton):
    kv_move = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.clicked.connect(self._activate_kv_move)

    def _activate_kv_move(self):
        self.kv_move.emit(1)


class ExitButton(QPushButton):
    myclicked = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.clicked.connect(self._activate_myclick)

    def _activate_myclick(self):
        self.myclicked.emit(4)


class MainWindow(QWidget):
    def __init__(self, train: Yauza, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.train = train
        self.err_timer = QTimer()
        self.err_timer.timeout.connect(self.clear_err)
        self.ticker = QTimer()
        self.ticker.timeout.connect(self.update_tick)
        self.update_tick()

        container = QGridLayout(self)

        self.speed_indicator = QLabel()
        self.update_speed()
        train.speed_changed_SIG.connect(self.update_speed)

        self.KV_indicator = QLabel()
        self.update_KV()
        train.kv_changed_SIG.connect(self.update_KV)

        self.RV_indicator = QLabel()
        self.update_RV()
        train.rv_changed_SIG.connect(self.update_RV)

        container.addWidget(self.speed_indicator, 0, 0)
        container.addWidget(self.KV_indicator, 0, 1)
        container.addWidget(self.RV_indicator, 0, 2)

        self.B_kv_forward = KVRVButton("KV forward")
        self.B_kv_forward.kv_move.connect(self.train.KV_forward)
        self.B_kv_back = KVRVButton("KV back")
        self.B_kv_back.kv_move.connect(self.train.KV_back)

        self.B_rv_forward = KVRVButton("RV forward")
        self.B_rv_forward.kv_move.connect(self.train.RV_forward)
        self.B_rv_back = KVRVButton("RV back")
        self.B_rv_back.kv_move.connect(self.train.RV_back)

        container.addWidget(self.B_kv_forward, 1, 1)
        container.addWidget(self.B_kv_back, 2, 1)

        container.addWidget(self.B_rv_forward, 1, 2)
        container.addWidget(self.B_rv_back, 2, 2)

        self.err_label = QLabel()
        self.update_err("None")
        train.rv_0_SIG.connect(self.update_err)
        train.kv_not_0_SIG.connect(self.update_err)
        container.addWidget(self.err_label, 3, 0, 3, 3)

        exit_button = ExitButton("Выйти")
        exit_button.myclicked.connect(self.close)
        container.addWidget(exit_button, 4, 0, 4, 3)

    def update_speed(self):
        v = self.train.curr_speed()
        self.speed_indicator.setText(f"speed: {v:.2f} km/h")

    def update_KV(self):
        self.KV_indicator.setText("KV pos: " + str(self.train.curr_kv()))

    def update_RV(self):
        self.RV_indicator.setText("RV pos: " + str(self.train.curr_rv()))

    def update_err(self, v):
        self.err_label.setText("Err: " + str(v))
        self.err_timer.start(2000)

    def clear_err(self):
        self.err_label.setText("")

    def update_tick(self):
        self.ticker.start(1000//4)
        rv = self.train.curr_rv()
        kv = self.train.curr_kv()
        speed = self.train.curr_speed()
        hod = kv > 0
        tormoz = kv < 0

        if rv != 0:
            if hod:
                self.train.change_speed(rv * kv)
            elif tormoz:
                if rv * speed <= 0:
                    self.train.change_speed(-speed)
                    return
                self.train.change_speed(rv*kv)
            speed = self.train.curr_speed()
        if abs(speed) < 0.1:
            if speed == 0:
                return
            self.train.change_speed(-speed)
            speed = self.train.curr_speed()
        # сила трения
        if speed > 0:
            self.train.change_speed(-max(0.0013*speed, 0.02))
        elif speed < 0:
            self.train.change_speed(max(0.0013*speed, 0.02))
