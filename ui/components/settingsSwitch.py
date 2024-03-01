from qtCore import *


class SwitchButton(QAbstractButton):
    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("switchButton")
        self.setFixedSize(56, 64)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._slider = QSlider()
        self._slider.setFixedWidth(56)
        self._slider.setOrientation(Qt.Horizontal)
        self._slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._slider.setMinimum(0)
        self._slider.setMaximum(1)
        self._slider.setEnabled(False)
        self._slider.valueChanged.connect(self.on_value_changed)
        self._layout.addWidget(self._slider)

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        if self._slider.value() == 0:
            self._slider.setValue(1)
        else:
            self._slider.setValue(0)

    @pyqtSlot(int)
    def on_value_changed(self, value):
        self.checkedChanged.emit(value == 1)

    def set_checked(self, a0: bool):
        if a0:
            self._slider.setValue(1)
        else:
            self._slider.setValue(0)

    def is_checked(self):
        return self._slider.value() == 1

    def paintEvent(self, e):
        pass

    # def mousePressEvent(self, a0: QMouseEvent) -> None:
    #     self.is_move = False
    #
    # def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
    #     if not self.is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
    #         self.clicked.emit()
    #
    # def mouseMoveEvent(self, a0: QMouseEvent) -> None:
    #     self.is_move = True


class SettingsSwitch(QFrame):
    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("settingsSwitch")
        self.setFixedHeight(64)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(20, 0, 10, 0)
        self._text = QLabel(self)
        self._text.setObjectName("switchLabel")
        self._layout.addWidget(self._text)
        self._slider = SwitchButton()
        self._slider.checkedChanged.connect(self.checkedChanged.emit)
        self._layout.addWidget(self._slider)

    def text(self):
        return self._text.text()

    def setText(self, text: str):
        self._text.setText(text)

    def setChecked(self, a0: bool):
        self._slider.set_checked(a0)

    def isChecked(self):
        return self._slider.is_checked()
