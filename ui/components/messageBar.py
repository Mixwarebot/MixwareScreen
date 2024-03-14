from qtCore import *


class MessageBar(QFrame):
    def __init__(self, index=0, text="", parent=None):
        super().__init__(parent)
        self.setObjectName("frameOutLine")
        self.setFixedHeight(60)

        self.serial_number_label = QLabel()
        self.text_label = QLabel()

        self.serial_number_label.setObjectName("serialNumber")
        self.serial_number_label.setFixedSize(40, 40)
        self.serial_number_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFixedWidth(255)
        self.text_label.setWordWrap(True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.serial_number_label)
        self.layout.addWidget(self.text_label)

        self.setIndex(index)
        self.setText(text)

    def setIndex(self, index: int):
        self.serial_number_label.setText(str(index))

    def setText(self, text: str):
        self.text_label.setText(text)
