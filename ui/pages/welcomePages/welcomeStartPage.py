from qtCore import *


class WelcomeStartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("welcomeStartPage.py")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-weight: bold; font-size: 32px;")
        self.layout.addWidget(self.title)
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setPixmap(QPixmap("resource/icon/Mixware").scaledToWidth(280))
        self.logo.setFixedSize(280, 960)
        self.layout.addWidget(self.logo)
        self.start_button = QPushButton()
        self.start_button.setFixedSize(280, 48)
        self.start_button.setStyleSheet("background-color: #FF5A00")
        self.layout.addWidget(self.start_button)
        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.title.setText(self.tr('Welcome'))
        self.start_button.setText(self.tr('Get started'))
