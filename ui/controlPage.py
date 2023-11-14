from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.fanPage import FanPage
from ui.filamentPage import FilamentPage
from ui.homePage import HomePage
from ui.levelPages.levelPage import LevelPage
from ui.levelPages.levelPreparePage import LevelPreParePage
from ui.movePage import MovePage
from ui.temperaturePage import TemperaturePage


class ControlPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("controlPage")

        self.temperatureButton = BasePushButton()
        self.fanButton = BasePushButton()
        self.filamentButton = BasePushButton()
        self.homeButton = BasePushButton()
        self.levelButton = BasePushButton()
        self.moveButton = BasePushButton()

        self.temperaturePage = TemperaturePage(self._printer, self._parent)
        self.fanPage = FanPage(self._printer, self._parent)
        self.filamentPage = FilamentPage(self._printer, self._parent)
        self.homePage = HomePage(self._printer, self._parent)
        self.levelPage = LevelPreParePage(self._printer, self._parent)
        self.movePage = MovePage(self._printer, self._parent)

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.temperatureButton.setObjectName("temperatureButton")
        self.fanButton.setObjectName("fanButton")
        self.filamentButton.setObjectName("filamentButton")
        self.homeButton.setObjectName("homeButton")
        self.levelButton.setObjectName("levelButton")
        self.moveButton.setObjectName("moveButton")
        self.reTranslateUi()

    def initLayout(self):
        button_layout = QGridLayout(self)
        button_layout.setContentsMargins(20, 0, 20, 0)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.temperatureButton, 0, 0)
        button_layout.addWidget(self.fanButton, 0, 1)
        button_layout.addWidget(self.filamentButton, 1, 0)
        button_layout.addWidget(self.homeButton, 1, 1)
        button_layout.addWidget(self.levelButton, 2, 0)
        button_layout.addWidget(self.moveButton, 2, 1)

    def initConnect(self):
        self.temperatureButton.clicked.connect(self.gotoTemperaturePage)
        self.fanButton.clicked.connect(self.gotoFanPage)
        self.filamentButton.clicked.connect(self.gotoFilamentPage)
        self.homeButton.clicked.connect(self.gotoHomePage)
        self.levelButton.clicked.connect(self.gotoLevelPage)
        self.moveButton.clicked.connect(self.gotoMovePage)

    @pyqtSlot()
    def gotoTemperaturePage(self):
        self._printer.write_gcode_command("D105")
        self._parent.gotoPage(self.temperaturePage, self.tr("Temperature"))

    @pyqtSlot()
    def gotoFilamentPage(self):
        self.filamentPage.backup_target()
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.tr("Filament"), self.tr("Whether preheating is required？\nPreheat temperature: 170°C"), buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self.filamentPage.need_preheat = True
            self._printer.write_gcode_command('M104 S170 T0\nM104 S170 T1')
        self._parent.closeShadowScreen()
        self._parent.gotoPage(self.filamentPage, self.tr("Filament"))

    @pyqtSlot()
    def gotoLevelPage(self):
        self._parent.gotoPage(self.levelPage, self.tr("Level Perpare"))

    @pyqtSlot()
    def gotoMovePage(self):
        self._printer.write_gcode_command("D114")
        self._parent.gotoPage(self.movePage, self.tr("Move"))

    @pyqtSlot()
    def gotoHomePage(self):
        self._parent.gotoPage(self.homePage, self.tr("Home"))

    @pyqtSlot()
    def gotoFanPage(self):
        self._printer.write_gcode_command("D106")
        self._parent.gotoPage(self.fanPage, self.tr("Fan"))

    def reTranslateUi(self):
        self.temperatureButton.setTitle(self.tr("Temperature"))
        self.fanButton.setTitle(self.tr("Fan"))
        self.filamentButton.setTitle(self.tr("Filament"))
        self.homeButton.setTitle(self.tr("Home"))
        self.levelButton.setTitle(self.tr("Level Prepare"))
        self.moveButton.setTitle(self.tr("Move"))

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()