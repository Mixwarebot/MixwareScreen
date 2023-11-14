from qtCore import *


class BaseTitle(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setObjectName("title")
