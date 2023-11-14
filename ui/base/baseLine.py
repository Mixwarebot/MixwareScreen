from qtCore import *


class BaseVLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(1)
        self.setObjectName("baseLine")

class BaseHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(1)
        self.setObjectName("baseLine")