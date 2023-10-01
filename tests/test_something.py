from PyQt6.QtCore import Qt 
import pytest
from yauza.gui.widgets import MainWindow
from yauza.gui.app import App
from yauza.train import Yauza 

@pytest.fixture
def train():
    return Yauza()


class TestSomething:
    def test_RV(self, qtbot, train):
        window = MainWindow(train)
        qtbot.addWidget(window)

        qtbot.mouseClick(window.B_rv_forward, Qt.MouseButton.LeftButton)
        assert window.RV_indicator.text() == "RV pos: 1"

        qtbot.mouseClick(window.B_rv_forward, Qt.MouseButton.LeftButton)
        assert window.RV_indicator.text() == "RV pos: 1"

        qtbot.mouseClick(window.B_rv_back, Qt.MouseButton.LeftButton)
        assert window.RV_indicator.text() == "RV pos: 0"

        qtbot.mouseClick(window.B_rv_back, Qt.MouseButton.LeftButton)
        assert window.RV_indicator.text() == "RV pos: -1"
    
    def test_KV(self, qtbot, train):
        window = MainWindow(train)
        qtbot.addWidget(window)

        qtbot.mouseClick(window.B_kv_forward, Qt.MouseButton.LeftButton)
        assert window.KV_indicator.text() == "KV pos: 0"

        qtbot.mouseClick(window.B_rv_forward, Qt.MouseButton.LeftButton)

        qtbot.mouseClick(window.B_kv_forward, Qt.MouseButton.LeftButton)
        assert window.KV_indicator.text() == "KV pos: 1"

        qtbot.mouseClick(window.B_kv_forward, Qt.MouseButton.LeftButton)
        assert window.KV_indicator.text() == "KV pos: 2"

        qtbot.mouseClick(window.B_kv_forward, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(window.B_kv_forward, Qt.MouseButton.LeftButton)
        assert window.KV_indicator.text() == "KV pos: 4"

        qtbot.mouseClick(window.B_kv_forward, Qt.MouseButton.LeftButton)
        assert window.KV_indicator.text() == "KV pos: 4"

        for _ in range(6):
            qtbot.mouseClick(window.B_kv_back, Qt.MouseButton.LeftButton)
        assert window.KV_indicator.text() == "KV pos: -2"
