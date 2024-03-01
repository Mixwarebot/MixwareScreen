from qtCore import *


class NotifyFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_move = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.notify = QLabel(self)
        self.notify.setFixedSize(360, 80)
        self.notify.setText(self.tr("This is a Mixware Screen message. Click anywhere to close it."))
        self.notify.setWordWrap(True)
        self.notify.setStyleSheet(
            "QLabel {background: rgba(0, 0, 0, 0.75); color: #FFFFFF; border: none; border-radius: 10px; padding-left: 20px;}")
        self.layout.addWidget(self.notify)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self.is_move = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            self.hide()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.is_move = True

    def set_text(self, text):
        self.notify.setText(text)
