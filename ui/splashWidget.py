from qtCore import *
from ui.base.baseLine import BaseHLine
from ui.base.basePushButton import BasePushButton


class SplashWidget(QWidget):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer

        self.resize(self._printer.config.get_window_size())
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(0)

        self.logo = QLabel()
        self.logo.setObjectName("splashLogo")
        self.logo.setFixedWidth(360)
        self.layout.addWidget(self.logo)

        self.layout.addSpacing(10)

        self.line = BaseHLine()
        self.line.setObjectName("splashLine")
        self.line.setFixedSize(360, 4)
        self.line.setStyleSheet("background: #FF5A00; border-radius: 2px; margin-left:120px;margin-right:120px;")
        self.layout.addWidget(self.line)

        self.layout.addSpacing(40)

        self.button = BasePushButton()
        self.button.setObjectName("splashButton")
        self.button.setFixedSize(360, 48)
        self.layout.addWidget(self.button)

        self.tips = QLabel()
        self.tips.setObjectName("tips")
        self.tips.setFixedWidth(360)
        self.tips.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.tips)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.button.setText(self.tr("Update"))
        self.tips.setText(self.tr("No printer detected."))
