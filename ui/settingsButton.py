from qtCore import *


class SettingsButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("settingsButton")

        self.setFlat(True)
        self.setFixedHeight(64)

        self._tips = QLabel(self)
        self._tips.setObjectName("tips")
        self._tips.setFixedSize(80, 24)
        self._tips.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.arrow = QLabel(self)
        self.arrow.setObjectName("arrowLogo")
        self.arrow.setFixedSize(24, 24)

    def tips(self):
        return self._tips.text()
    def setTips(self, text: str):
        self._tips.setText(text)

    def resizeEvent(self, event) -> None:
        self._tips.move(self.width() - self._tips.width() - self.arrow.width() - 2, (self.height() - self._tips.height()) / 2)
        self.arrow.move(self.width() - self.arrow.width(), (self.height() - self.arrow.height()) / 2)
