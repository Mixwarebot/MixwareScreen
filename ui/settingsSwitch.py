from qtCore import *


class SwitchButton(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.is_move = None
        self.setObjectName("switchButton")


    # def mousePressEvent(self, a0: QMouseEvent) -> None:
    #     self.is_move = False
    #
    # def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
    #     if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
    #         self.clicked.emit()
    #
    # def mouseMoveEvent(self, a0: QMouseEvent) -> None:
    #     self.is_move = True

class SettingsSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("settingsSwitch")

        self.setFixedHeight(64)

    # def resizeEvent(self, event) -> None:
    #     self._tips.move(self.width() - self._tips.width() - self.arrow.width() - 2, (self.height() - self._tips.height()) / 2)
    #     self.arrow.move(self.width() - self.arrow.width(), (self.height() - self.arrow.height()) / 2)
