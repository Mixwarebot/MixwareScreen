from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.temperatureBox import TemperatureBox
from ui.controlPage import ControlPage
from ui.printFilePage import PrintFilePage
from ui.settingsPage import SettingsPage



class PrinterPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("printerPage")

        self.temperatureWidget = TemperatureBox(self._printer)
        self.printButton = BasePushButton()
        self.controlButton = BasePushButton()
        self.setButton = BasePushButton()

        self.printFilePage = PrintFilePage(self._printer, self._parent)
        self.controlPage = ControlPage(self._printer, self._parent)
        self.settingsPage = SettingsPage(self._printer, self._parent)

        QScroller.grabGesture(self.printFilePage, QScroller.TouchGesture)

        self.initForm()
        self.initLayout()
        self.initConnect()

    def reTranslateUi(self):
        self.printButton.setTitle(self.tr("Print"))
        self.controlButton.setTitle(self.tr("Control"))
        self.setButton.setTitle(self.tr("Settings"))
        # self.printButton.setTitle(QtCore.QCoreApplication.translate("printerPage", "Print"))
        # self.controlButton.setTitle(QtCore.QCoreApplication.translate("printerPage", "Control"))
        # self.setButton.setTitle(QtCore.QCoreApplication.translate("printerPage", "Settings"))

    def initForm(self):
        self.reTranslateUi()

        self.printButton.setObjectName("printButton")
        self.controlButton.setObjectName("controlButton")
        self.setButton.setObjectName("setButton")

    def initLayout(self):
        button_layout = QGridLayout()
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.printButton, 0, 0, 1, 2)
        button_layout.addWidget(self.controlButton, 1, 0, 1, 1)
        button_layout.addWidget(self.setButton, 1, 1, 1, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 20)
        layout.setSpacing(0)
        layout.addWidget(self.temperatureWidget, 4)
        layout.addLayout(button_layout, 5)

    def initConnect(self):
        self.temperatureWidget.left.clicked.connect(self._parent.open_thermal_left_numberPad)
        self.temperatureWidget.right.clicked.connect(self._parent.open_thermal_right_numberPad)
        self.temperatureWidget.bed.clicked.connect(self._parent.open_thermal_bed_numberPad)
        self.temperatureWidget.chamber.clicked.connect(self._parent.open_thermal_chamber_numberPad)

        self.printButton.clicked.connect(self.gotoPrintFilePage)
        self.controlButton.clicked.connect(self.gotoControlPage)
        self.setButton.clicked.connect(self.gotoSettingsPage)

    @pyqtSlot()
    def gotoPrintFilePage(self):
        self._parent.gotoPage(self.printFilePage, "File")

    @pyqtSlot()
    def gotoControlPage(self):
        self._parent.gotoPage(self.controlPage, "Control")

    @pyqtSlot()
    def gotoSettingsPage(self):
        self._parent.gotoPage(self.settingsPage, "Settings")

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()