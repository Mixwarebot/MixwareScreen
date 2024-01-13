from qtCore import *


class BaseRoundDialog(QDialog):
    def __init__(self, parent, radius_x=0, radius_y=0, color="#999999", alpha=1.0):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.color = QColor(color)
        self.color.setAlphaF(alpha)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.transparent)
        rect = self.rect()
        rect.setWidth(rect.width())
        rect.setHeight(rect.height())
        painter.drawRoundedRect(rect, self.radius_x, self.radius_y)


class BaseRoundWidget(QWidget):
    def __init__(self, parent, radius_x=10, radius_y=10, color="#FFFFFF", alpha=1.0):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.color = QColor(color)
        self.color.setAlphaF(alpha)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.transparent)
        rect = self.rect()
        rect.setWidth(rect.width())
        rect.setHeight(rect.height())
        painter.drawRoundedRect(rect, self.radius_x, self.radius_y)
