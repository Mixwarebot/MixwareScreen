from qtCore import *
from ui.base.basePushButton import BasePushButton


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
class SplashWidget(QWidget):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self.line_width = 80
        self.line_height = 4

        self.logo = QLabel()
        self.button = BasePushButton()
        self.tips = QLabel()
        self.line = QLabel()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.logo.setObjectName("splashLogo")
        self.button.setObjectName("splashButton")
        self.line.setStyleSheet("QLabel{image: url(resource/icon/line); color: #FF5A00}")
        self.tips.setObjectName("tips")
        self.button.setText(self.tr("Update"))
        self.tips.setText(self.tr("No printer detected."))

        self.logo.setFixedHeight(40)
        self.line.setFixedHeight(3)
        self.button.setFixedSize(300, 48)
        self.tips.setFixedHeight(32)

        self.tips.setAlignment(Qt.AlignCenter)
        self.resize(self._printer.config.get_window_size())

    def initLayout(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.logo)
        layout.addSpacing(10)
        layout.addWidget(self.line)
        layout.addSpacing(35)
        layout.addWidget(self.button)
        layout.addWidget(self.tips)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

    def initConnect(self):
        pass
