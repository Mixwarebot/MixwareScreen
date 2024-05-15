from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.pages.fanPage import FanPage
from ui.pages.filamentPage import FilamentPage
from ui.pages.homePage import HomePage
from ui.pages.leveling.levelPreparePage import LevelPreParePage
from ui.pages.movePage import MovePage
from ui.pages.temperaturePage import TemperaturePage


class ControlPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("controlPage")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.temperatureButton = BasePushButton()
        self.temperatureButton.setObjectName("temperatureButton")
        self.temperatureButton.clicked.connect(self.goto_temperature_page)
        self.layout.addWidget(self.temperatureButton, 0, 0)

        self.fanButton = BasePushButton()
        self.fanButton.setObjectName("fanButton")
        self.fanButton.clicked.connect(self.goto_fan_page)
        self.layout.addWidget(self.fanButton, 0, 1)

        self.filamentButton = BasePushButton()
        self.filamentButton.setObjectName("filamentButton")
        self.filamentButton.clicked.connect(self.goto_filament_page)
        self.layout.addWidget(self.filamentButton, 1, 0)

        self.homeButton = BasePushButton()
        self.homeButton.setObjectName("homeButton")
        self.homeButton.clicked.connect(self.goto_home_page)
        self.layout.addWidget(self.homeButton, 1, 1)

        self.levelButton = BasePushButton()
        self.levelButton.setObjectName("levelButton")
        self.levelButton.clicked.connect(self.goto_level_page)
        self.layout.addWidget(self.levelButton, 2, 0)

        self.moveButton = BasePushButton()
        self.moveButton.setObjectName("moveButton")
        self.moveButton.clicked.connect(self.goto_move_page)
        self.layout.addWidget(self.moveButton, 2, 1)

        self.temperature_page = TemperaturePage(self._printer, self._parent)
        self.fan_page = FanPage(self._printer, self._parent)
        self.filament_page = FilamentPage(self._printer, self._parent)
        self.home_page = HomePage(self._printer, self._parent)
        self.level_page = LevelPreParePage(self._printer, self._parent)
        self.move_page = MovePage(self._printer, self._parent)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.temperatureButton.setTitle(self.tr("Temperature"))
        self.fanButton.setTitle(self.tr("Fan"))
        self.filamentButton.setTitle(self.tr("Filament"))
        self.homeButton.setTitle(self.tr("Home"))
        self.levelButton.setTitle(self.tr("Level"))
        self.moveButton.setTitle(self.tr("Move"))

    @pyqtSlot()
    def goto_temperature_page(self):
        self._printer.write_gcode_command("D105")
        self._parent.gotoPage(self.temperature_page, self.tr("Temperature"))

    @pyqtSlot()
    def goto_filament_page(self):
        self.filament_page.backup_target()
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.tr("Filament"),
                                         self.tr("Preheating or not?\nPreheating temperature 170°C"),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self.filament_page.need_preheat = True
            self._printer.write_gcode_command('M104 S170 T0\nM104 S170 T1')
        self._parent.closeShadowScreen()
        self._parent.gotoPage(self.filament_page, self.tr("Filament"))

    @pyqtSlot()
    def goto_level_page(self):
        self._parent.gotoPage(self.level_page, self.tr("Leveling Prepare"))

    @pyqtSlot()
    def goto_move_page(self):
        self._printer.write_gcode_command("D114")
        self._parent.gotoPage(self.move_page, self.tr("Move"))

    @pyqtSlot()
    def goto_home_page(self):
        self._parent.gotoPage(self.home_page, self.tr("Home"))

    @pyqtSlot()
    def goto_fan_page(self):
        self._printer.write_gcode_command("D106")
        self._parent.gotoPage(self.fan_page, self.tr("Fan"))
