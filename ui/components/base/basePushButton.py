from qtCore import *


class BasePushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(40)
        self.title.setStyleSheet("font-size: 21px;")
        self.title.hide()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignBottom)
        layout.setContentsMargins(10, 0, 10, 20)
        layout.addWidget(self.title)

    def setTitle(self, text: str):
        self.title.setText(text)
        if text:
            self.title.show()
        else:
            self.title.hide()
