from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.base.baseRound import BaseRoundWidget

class FanBar(BaseRoundWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(128)

        self.title = QLabel()
        self.title.setFixedHeight(40)
        self.title.setObjectName("title")

        self.imageButton = BasePushButton()
        self.imageButton.setFlat(True)
        self.imageButton.setObjectName("fanButton")
        self.imageButton.setFixedSize(self.height() - self.title.height(), self.height() - self.title.height())

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.hBoxLayout.setSpacing(10)
        self.hBoxLayout.addWidget(self.imageButton)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.title, 0, 0)
        self.layout.addLayout(self.hBoxLayout, 1, 0)
        self.setLayout(self.layout)

        self.tips = QLabel(self)
        self.tips.setFixedSize(80, 40)
        self.tips.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tips.setText("100%")

    def setTitle(self, text: str):
        self.title.setText(text)

    def setTips(self, text: str):
        self.tips.setText(text)

    def resizeEvent(self, event) -> None:
        self.tips.move(self.width() - self.tips.width() - 20, 0)
        self.imageButton.setFixedSize(self.height() - self.title.height(), self.height() - self.title.height())
        self.imageButton.setStyleSheet(f"qproperty-iconSize: {self.imageButton.width()}px {self.imageButton.height()}px;")

class FanProgressBar(FanBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)

        self.hBoxLayout.addWidget(self.progressBar)

    def setFanSpeed(self, speed: int):
        self.progressBar.setValue(int(speed*100))
        self.setTips(str(int(speed*100))+"%")

class FanSliderBar(FanBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.hBoxLayout.addWidget(self.slider)

    def setFanSpeed(self, speed: int):
        self.slider.setValue(int(speed*100))
        self.setTips(str(int(speed*100))+"%")

class FanPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("fanPage")

        self.modelFanLeftSpeed = 0
        self.modelFanRightSpeed = 0
        self.exhaustFanSpeed = 0

        self.extruderFanLeft = FanProgressBar()
        self.extruderFanRight = FanProgressBar()
        self.chamberFan = FanProgressBar()
        self.motherboardFan = FanProgressBar()
        self.modelFanLeft = FanSliderBar()
        self.modelFanRight = FanSliderBar()
        self.exhaustFan = FanSliderBar()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.extruderFanLeft.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.extruderFanLeft.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.extruderFanLeft.imageButton.setObjectName("fanLeftLogo")

        self.extruderFanRight.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.extruderFanRight.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.extruderFanRight.imageButton.setObjectName("fanRightLogo")

        self.chamberFan.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.chamberFan.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.chamberFan.imageButton.setObjectName("fanChamberLogo")

        self.motherboardFan.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.motherboardFan.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.motherboardFan.imageButton.setObjectName("fanChamberLogo")

        self.modelFanLeft.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.modelFanLeft.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.modelFanLeft.imageButton.setObjectName("fanLeftLogo")

        self.modelFanRight.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.modelFanRight.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.modelFanRight.imageButton.setObjectName("fanRightLogo")

        self.exhaustFan.resize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.exhaustFan.setFixedSize(self._printer.config.get_width()-40, self._printer.config.get_height() / 10)
        self.exhaustFan.imageButton.setObjectName("fanExhaustLogo")

        self.updateFanSpeed()
        self.reTranslateUi()

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)

        layout.addWidget(self.extruderFanLeft)
        layout.addWidget(self.extruderFanRight)
        layout.addWidget(self.chamberFan)
        layout.addWidget(self.motherboardFan)
        layout.addWidget(self.modelFanLeft)
        layout.addWidget(self.modelFanRight)
        layout.addWidget(self.exhaustFan)

    def initConnect(self):
        self.modelFanLeft.slider.valueChanged.connect(self.changeModelLeftFanSpeed)
        self.modelFanLeft.slider.sliderReleased.connect(self.setModelLeftFanSpeed)
        self.modelFanLeft.imageButton.clicked.connect(self.modelLeftFanOnOff)
        self.modelFanRight.slider.valueChanged.connect(self.changeModelRightFanSpeed)
        self.modelFanRight.slider.sliderReleased.connect(self.setModelRightFanSpeed)
        self.modelFanRight.imageButton.clicked.connect(self.modelRightFanOnOff)
        self.exhaustFan.slider.valueChanged.connect(self.changeExhaustFanSpeed)
        self.exhaustFan.slider.sliderReleased.connect(self.setExhaustFanSpeed)
        self.exhaustFan.imageButton.clicked.connect(self.exhaustFanOnOff)
        self._printer.updatePrinterInformation.connect(self.updateFanSpeed)

    @pyqtSlot()
    def modelLeftFanOnOff(self):
        if self.modelFanLeftSpeed == 0:
            self.modelFanLeftSpeed = 1
        else:
            self.modelFanLeftSpeed = 0
        self.setModelLeftFanSpeed()

    @pyqtSlot()
    def modelRightFanOnOff(self):
        if self.modelFanRightSpeed == 0:
            self.modelFanRightSpeed = 1
        else:
            self.modelFanRightSpeed = 0
        self.setModelRightFanSpeed()

    @pyqtSlot()
    def exhaustFanOnOff(self):
        if self.exhaustFanSpeed == 0:
            self.exhaustFanSpeed = 1
        else:
            self.exhaustFanSpeed = 0
        self.setExhaustFanSpeed()

    @pyqtSlot(int)
    def changeModelLeftFanSpeed(self, value):
        self.modelFanLeftSpeed = value / 100

    @pyqtSlot()
    def setModelLeftFanSpeed(self):
        self._printer.set_fan_speed("left", self.modelFanLeftSpeed)

    @pyqtSlot(int)
    def changeModelRightFanSpeed(self, value):
        self.modelFanRightSpeed = value / 100

    @pyqtSlot()
    def setModelRightFanSpeed(self):
        self._printer.set_fan_speed("right", self.modelFanRightSpeed)

    @pyqtSlot(int)
    def changeExhaustFanSpeed(self, value):
        self.exhaustFanSpeed = value / 100

    @pyqtSlot()
    def setExhaustFanSpeed(self):
        self._printer.set_fan_speed("exhaust", self.exhaustFanSpeed)

    @pyqtSlot()
    def updateFanSpeed(self):
        self.extruderFanLeft.setFanSpeed(self._printer.get_fan_speed("leftCool"))
        self.extruderFanRight.setFanSpeed(self._printer.get_fan_speed("rightCool"))
        self.chamberFan.setFanSpeed(self._printer.get_fan_speed("chamber"))
        self.motherboardFan.setFanSpeed(self._printer.get_fan_speed("chamber"))
        self.modelFanLeft.setFanSpeed(self._printer.get_fan_speed("left"))
        self.modelFanRight.setFanSpeed(self._printer.get_fan_speed("right"))
        self.exhaustFan.setFanSpeed(self._printer.get_fan_speed("exhaust"))

    def reTranslateUi(self):
        self.extruderFanLeft.setTitle(self.tr("Extruder Fan(Left)"))
        self.extruderFanRight.setTitle(self.tr("Extruder Fan(Right)"))
        self.chamberFan.setTitle(self.tr("Chamber Fan"))
        self.motherboardFan.setTitle(self.tr("Motherboard Fan"))
        self.modelFanLeft.setTitle(self.tr("Model Fan(Left)"))
        self.modelFanRight.setTitle(self.tr("Model Fan(Right)"))
        self.exhaustFan.setTitle(self.tr("Exhaust Fan"))

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()
