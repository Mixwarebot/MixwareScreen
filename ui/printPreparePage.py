from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.fanPage import FanPage
from ui.filamentPage import FilamentPage
from ui.homePage import HomePage
from ui.levelPages.levelPage import LevelPage
from ui.levelPages.levelPreparePage import LevelPreParePage
from ui.movePage import MovePage
from ui.printFilePage import PrintFilePage
from ui.temperaturePage import TemperaturePage


class PrintPreparePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("printPreParePage")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.local_button = BasePushButton()
        # self.local_button.setObjectName("temperatureButton")
        self.layout.addWidget(self.local_button, 0, 0)

        self.usb_button = BasePushButton()
        # self.usb_button.setObjectName("fanButton")
        self.layout.addWidget(self.usb_button, 0, 1)

        self.xy_button = BasePushButton()
        # self.xy_button.setObjectName("filamentButton")
        self.xy_button.clicked.connect(self.print_xy_verity)
        self.layout.addWidget(self.xy_button, 1, 0)

        # self.homeButton = BasePushButton()
        # self.homeButton.setObjectName("homeButton")
        # self.homeButton.clicked.connect(self.goto_home_page)
        # self.layout.addWidget(self.homeButton, 1, 1)
        #
        # self.levelButton = BasePushButton()
        # self.levelButton.setObjectName("levelButton")
        # self.levelButton.clicked.connect(self.goto_level_page)
        # self.layout.addWidget(self.levelButton, 2, 0)
        #
        # self.moveButton = BasePushButton()
        # self.moveButton.setObjectName("moveButton")
        # self.moveButton.clicked.connect(self.goto_move_page)
        # self.layout.addWidget(self.moveButton, 2, 1)

        self.printFilePage = PrintFilePage(self._printer, self._parent)
        QScroller.grabGesture(self.printFilePage, QScroller.TouchGesture)

        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.local_button.setText(self.tr("Local Print"))
        self.usb_button.setText(self.tr("USB Print"))
        self.xy_button.setText(self.tr("XY Verity"))
        # self.homeButton.setTitle(self.tr("Home"))
        # self.levelButton.setTitle(self.tr("Level"))
        # self.moveButton.setTitle(self.tr("Move"))

    @pyqtSlot()
    def print_xy_verity(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start("Mixware Screen", self.tr("Verity XY offset ?"), buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.print_start('resource/gcode/print_verify.gcode')
        self._parent.closeShadowScreen()