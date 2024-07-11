from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.pages.printPreparePage import PrintPreparePage
from ui.components.temperatureWidget import TemperatureWidget
from ui.pages.controlPage import ControlPage
from ui.pages.printFilePage import PrintFilePage
from ui.pages.settingsPage import SettingsPage


class PrinterPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("printerPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 20)
        self.layout.setSpacing(0)
        self.temperatureWidget = TemperatureWidget(self._printer)
        self.temperatureWidget.left.clicked.connect(self._parent.open_thermal_left_numberPad)
        self.temperatureWidget.right.clicked.connect(self._parent.open_thermal_right_numberPad)
        self.temperatureWidget.bed.clicked.connect(self._parent.open_thermal_bed_numberPad)
        self.temperatureWidget.chamber.clicked.connect(self._parent.open_thermal_chamber_numberPad)
        self.layout.addWidget(self.temperatureWidget, 4)
        self.button_layout = QGridLayout()
        self.button_layout.setContentsMargins(0, 10, 0, 10)
        self.button_layout.setSpacing(10)
        self.printButton = BasePushButton()
        self.printButton.setObjectName("printButton")

        self.printPreparePage = PrintPreparePage(self._printer, self._parent)
        self.printPreparePage.local_button.clicked.connect(self.goto_local_print_page)
        self.printPreparePage.usb_button.clicked.connect(self.goto_usb_print_page)
        self.printFilePage = PrintFilePage(self._printer, self._parent)
        QScroller.grabGesture(self.printFilePage, QScroller.TouchGesture)
        self.printButton.clicked.connect(self.goto_print_prepare_page)
        self.button_layout.addWidget(self.printButton, 0, 0, 1, 2)
        self.controlButton = BasePushButton()
        self.controlButton.setObjectName("controlButton")
        self.controlPage = ControlPage(self._printer, self._parent)
        self.controlButton.clicked.connect(self.goto_control_page)
        self.button_layout.addWidget(self.controlButton, 1, 0, 1, 1)
        self.setButton = BasePushButton()
        self.setButton.setObjectName("setButton")
        self.settingsPage = SettingsPage(self._printer, self._parent)
        self.setButton.clicked.connect(self.goto_settings_page)
        self.button_layout.addWidget(self.setButton, 1, 1, 1, 1)
        self.layout.addLayout(self.button_layout, 5)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.printButton.setTitle(self.tr("Print"))
        self.controlButton.setTitle(self.tr("Control"))
        self.setButton.setTitle(self.tr("Settings"))

    @pyqtSlot()
    def goto_print_prepare_page(self):
        self._parent.gotoPage(self.printPreparePage, self.tr("Print Prepare"))

    @pyqtSlot()
    def goto_local_print_page(self):
        self.printFilePage.set_local_path()
        self._parent.gotoPage(self.printFilePage, self.tr("Local Print"))

    @pyqtSlot()
    def goto_usb_print_page(self):
        self.printFilePage.set_usb_path()
        self._parent.gotoPage(self.printFilePage, self.tr("USB Print"))

    @pyqtSlot()
    def goto_control_page(self):
        self._parent.gotoPage(self.controlPage, self.tr("Control"))

    @pyqtSlot()
    def goto_settings_page(self):
        self._parent.gotoPage(self.settingsPage, self.tr("Settings"))
        self._printer.write_gcode_command("M503")
