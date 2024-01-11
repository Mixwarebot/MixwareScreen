from qtCore import *
from ui.base.baseLine import BaseHLine


class HeaderBar(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_move = None
        self.setFixedHeight(84)

        self.title = QLabel()
        self.title.setText("Mixware Screen")
        self.title.setFixedHeight(64)
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 4)
        layout.addWidget(self.title)
        layout.addWidget(BaseHLine())

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.is_move = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            self.clicked.emit()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.is_move = True
