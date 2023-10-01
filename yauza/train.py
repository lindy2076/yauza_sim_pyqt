from PyQt6.QtCore import QObject, pyqtSignal


class Yauza(QObject):
    speed_changed_SIG = pyqtSignal(int)
    kv_changed_SIG = pyqtSignal(int)
    rv_changed_SIG = pyqtSignal(int)

    rv_0_SIG = pyqtSignal(str)
    kv_not_0_SIG = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.speed = 0
        self.KV = 0
        self.RV = 0
        self.brakes = True

    def curr_speed(self):
        return self.speed

    def curr_kv(self):
        return self.KV

    def curr_rv(self):
        return self.RV

    def curr_brakes(self):
        return self.brakes

    def KV_forward(self):
        if self.RV == 0:
            return self._notify_rv_0()
        if self.KV == 4:
            return
        self.KV += 1
        self._notify_kv_changed(self.KV)

    def KV_back(self):
        if self.RV == 0:
            return self._notify_rv_0()
        if self.KV == -3:
            return
        self.KV -= 1
        self._notify_kv_changed(self.KV)

    def RV_forward(self):
        if self.KV != 0:
            return self._notify_kv_not_0()
        if self.RV == 1:
            return
        self.RV += 1
        self._notify_rv_changed(self.RV)

    def RV_back(self):
        if self.KV != 0:
            return self._notify_kv_not_0()
        if self.RV == -1:
            return
        self.RV -= 1
        self._notify_rv_changed(self.RV)

    def change_speed(self, v):
        self.speed += v
        self._notify_speed_change(v)

    def _notify_speed_change(self, v):
        self.speed_changed_SIG.emit(v)

    def _notify_kv_changed(self, v):
        self.kv_changed_SIG.emit(v)

    def _notify_rv_changed(self, v):
        self.rv_changed_SIG.emit(v)

    def _notify_rv_0(self):
        self.rv_0_SIG.emit("rv 0!")

    def _notify_kv_not_0(self):
        self.kv_not_0_SIG.emit("kv not 0!")
