from qtCore import *
from ui.base.basePushButton import BasePushButton


class FanProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(178)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title = QLabel()
        self.title.setFixedHeight(48)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox {margin: 0 10px 0 10px}")
        self.hBoxLayout = QVBoxLayout(self.frame)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setAlignment(Qt.AlignCenter)
        self.imageButton = BasePushButton()
        self.imageButton.setFlat(True)
        self.imageButton.setFixedSize(84, 84)
        self.imageButton.setStyleSheet("QPushButton { qproperty-iconSize: 72px 72px; }")
        self.hBoxLayout.addWidget(self.imageButton)

        self.tips = QLabel()
        self.tips.setFixedHeight(40)
        self.tips.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.tips)
        self.layout.addWidget(self.frame)

    def set_title(self, text: str):
        self.title.setText(text)

    def set_tips(self, text: str):
        self.tips.setText(text)

    def set_fan_speed(self, speed: int):
        self.set_tips(str(int(speed * 100)) + "%")


class FanSliderBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(148)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.title = QLabel()
        self.title.setFixedHeight(40)
        self.layout.addWidget(self.title, 0, 0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.hBoxLayout = QHBoxLayout(self.frame)
        self.hBoxLayout.setContentsMargins(10, 0, 10, 0)
        self.hBoxLayout.setSpacing(10)
        self.imageButton = BasePushButton()
        self.imageButton.setFlat(True)
        self.imageButton.setFixedSize(84, 84)
        self.imageButton.setStyleSheet("QPushButton { qproperty-iconSize: 72px 72px; }")
        self.hBoxLayout.addWidget(self.imageButton)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.hBoxLayout.addWidget(self.slider)
        self.layout.addWidget(self.frame, 1, 0)

        self.tips = QLabel(self)
        self.tips.setFixedSize(80, 40)
        self.tips.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tips.setText("100%")

    def resizeEvent(self, event) -> None:
        self.tips.move(self.width() - self.tips.width() - 30, 0)

    def set_title(self, text: str):
        self.title.setText(text)

    def set_tips(self, text: str):
        self.tips.setText(text)

    def set_fan_speed(self, speed: int):
        self.slider.setValue(int(speed * 100))
        self.set_tips(str(int(speed * 100)) + "%")


class FanPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.update_fan_speed)

        self._parent = parent

        self.setObjectName("fanPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 20, 0, 20)
        self.frame_layout.setSpacing(10)
        self.frame_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.modelFanLeftSpeed = 0
        self.modelFanRightSpeed = 0
        self.exhaustFanSpeed = 0

        self.layout_1 = QHBoxLayout()
        self.layout_1.setContentsMargins(10, 0, 10, 0)
        self.layout_1.setSpacing(0)
        self.extruderFanLeft = FanProgressBar()
        self.extruderFanLeft.imageButton.setObjectName("fanLeftLogo")
        self.layout_1.addWidget(self.extruderFanLeft)

        self.extruderFanRight = FanProgressBar()
        self.extruderFanRight.imageButton.setObjectName("fanRightLogo")
        self.layout_1.addWidget(self.extruderFanRight)
        self.frame_layout.addLayout(self.layout_1)

        self.layout_2 = QHBoxLayout()
        self.layout_2.setContentsMargins(10, 0, 10, 0)
        self.layout_2.setSpacing(0)
        self.chamberFan = FanProgressBar()
        self.chamberFan.imageButton.setObjectName("fanChamberLogo")
        self.layout_2.addWidget(self.chamberFan)

        self.motherboardFan = FanProgressBar()
        self.motherboardFan.imageButton.setObjectName("fanBoardLogo")
        self.layout_2.addWidget(self.motherboardFan)
        self.frame_layout.addLayout(self.layout_2)

        self.modelFanLeft = FanSliderBar()
        self.modelFanLeft.imageButton.setObjectName("fanModelLeftLogo")
        self.modelFanLeft.slider.valueChanged.connect(self.change_model_left_fan_speed)
        self.modelFanLeft.slider.sliderReleased.connect(self.set_model_left_fan_speed)
        self.modelFanLeft.imageButton.clicked.connect(self.model_left_fan_on_off)
        self.frame_layout.addWidget(self.modelFanLeft)

        self.modelFanRight = FanSliderBar()
        self.modelFanRight.imageButton.setObjectName("fanModelRightLogo")
        self.modelFanRight.slider.valueChanged.connect(self.change_model_right_fan_speed)
        self.modelFanRight.slider.sliderReleased.connect(self.set_model_right_fan_speed)
        self.modelFanRight.imageButton.clicked.connect(self.model_right_fan_on_off)
        self.frame_layout.addWidget(self.modelFanRight)

        self.exhaustFan = FanSliderBar()
        self.exhaustFan.imageButton.setObjectName("fanExhaustLogo")
        self.exhaustFan.slider.valueChanged.connect(self.change_exhaust_fan_speed)
        self.exhaustFan.slider.sliderReleased.connect(self.set_exhaust_fan_speed)
        self.exhaustFan.imageButton.clicked.connect(self.exhaust_fan_on_off)
        self.frame_layout.addWidget(self.exhaustFan)
        self.layout.addWidget(self.frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.extruderFanLeft.set_title(self.tr("Extruder Fan\n(Left)"))
        self.extruderFanRight.set_title(self.tr("Extruder Fan\n(Right)"))
        self.chamberFan.set_title(self.tr("Chamber Fan"))
        self.motherboardFan.set_title(self.tr("Main-board Fan"))
        self.modelFanLeft.set_title(self.tr("Model Fan(Left)"))
        self.modelFanRight.set_title(self.tr("Model Fan(Right)"))
        self.exhaustFan.set_title(self.tr("Exhaust Fan"))

    @pyqtSlot()
    def model_left_fan_on_off(self):
        self.modelFanLeftSpeed = 1 if self.modelFanLeftSpeed == 0 else 0
        self.set_model_left_fan_speed()

    @pyqtSlot()
    def model_right_fan_on_off(self):
        self.modelFanRightSpeed = 1 if self.modelFanRightSpeed == 0 else 0
        self.set_model_right_fan_speed()

    @pyqtSlot()
    def exhaust_fan_on_off(self):
        self.exhaustFanSpeed = 1 if self.exhaustFanSpeed == 0 else 0
        self.set_exhaust_fan_speed()

    @pyqtSlot(int)
    def change_model_left_fan_speed(self, value):
        self.modelFanLeftSpeed = value / 100

    @pyqtSlot()
    def set_model_left_fan_speed(self):
        self._printer.set_fan_speed("left", self.modelFanLeftSpeed)

    @pyqtSlot(int)
    def change_model_right_fan_speed(self, value):
        self.modelFanRightSpeed = value / 100

    @pyqtSlot()
    def set_model_right_fan_speed(self):
        self._printer.set_fan_speed("right", self.modelFanRightSpeed)

    @pyqtSlot(int)
    def change_exhaust_fan_speed(self, value):
        self.exhaustFanSpeed = value / 100

    @pyqtSlot()
    def set_exhaust_fan_speed(self):
        self._printer.set_fan_speed("exhaust", self.exhaustFanSpeed)

    @pyqtSlot()
    def update_fan_speed(self):
        if not self.isVisible():
            return
        self.extruderFanLeft.set_fan_speed(self._printer.get_fan_speed("leftCool"))
        self.extruderFanRight.set_fan_speed(self._printer.get_fan_speed("rightCool"))
        self.chamberFan.set_fan_speed(self._printer.get_fan_speed("chamber"))
        self.motherboardFan.set_fan_speed(self._printer.get_fan_speed("chamber"))
        self.modelFanLeft.set_fan_speed(self._printer.get_fan_speed("left"))
        self.modelFanRight.set_fan_speed(self._printer.get_fan_speed("right"))
        self.exhaustFan.set_fan_speed(self._printer.get_fan_speed("exhaust"))
