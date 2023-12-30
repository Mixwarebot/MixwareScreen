import logging

from qtCore import *
from ui.base.baseMessageBox import BaseMessageBox
from ui.footerBar import FooterBar
from ui.headerBar import HeaderBar
from ui.numberPad import NumberPad


class BasePrintWidget(QWidget):
    openPopup = pyqtSignal()

    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self.resize(self._printer.config.get_window_size())

        self.header = HeaderBar()
        self.header.setObjectName("header")
        self.header_title_queue = []
        self.content = QFrame()
        self.stackedLayout = QStackedLayout(self.content)
        self.footer = FooterBar()
        self.footer.setObjectName("footer")

        self.message = BaseMessageBox(self._printer)
        self.message.setObjectName("message")

        self.numberPad = NumberPad(self._printer)
        self.numberPad.setObjectName("numberPad")
        self.numberPad.rejected.connect(self.closeShadowScreen)

        self.shadowScreen = QLabel(self)
        self.shadowScreen.setObjectName("shadowScreen")
        self.shadowScreen.setFixedSize(self.size())
        self.shadowScreen.hide()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.content)
        self.layout.addWidget(self.footer, Qt.AlignBottom)

        self.header.clicked.connect(self.on_header_clicked)

        self.footer.mainButton.clicked.connect(self.gotoMainPage)
        self.footer.reboot_stop_button.clicked.connect(self.on_reboot_button_clicked)

    def gotoPage(self, page: QWidget, text: str, show=True):
        self.stackedLayout.addWidget(page)
        self.stackedLayout.setCurrentWidget(page)
        self.header_title_queue.append(self.header.title.text())
        self.header.title.setText(text)
        logging.info(f"Goto {self.stackedLayout.currentWidget().objectName()}")
        if show:
            self.footer.show()

    def exitPage(self):
        self.stackedLayout.removeWidget(self.stackedLayout.currentWidget())
        self.header.title.setText(self.header_title_queue[-1])
        self.header_title_queue.remove(self.header_title_queue[-1])
        logging.info(f"Goto {self.stackedLayout.currentWidget().objectName()}")

    @pyqtSlot()
    def gotoMainPage(self):
        while self.stackedLayout.count() > 1:
            self.exitPage()

        self.footer.hide()

    @pyqtSlot()
    def gotoPreviousPage(self):
        if self.stackedLayout.count() > 1:
            self.exitPage()
        if self.stackedLayout.count() == 1:
            self.footer.hide()

    def open_thermal_left_numberPad(self):
        if not self.numberPad.isVisible():
            self.showShadowScreen()
            self.numberPad.start("", "thermal_left")

    def open_thermal_right_numberPad(self):
        if not self.numberPad.isVisible():
            self.showShadowScreen()
            self.numberPad.start("", "thermal_right")

    def open_thermal_bed_numberPad(self):
        if not self.numberPad.isVisible():
            self.showShadowScreen()
            self.numberPad.start("", "thermal_bed")

    def open_thermal_chamber_numberPad(self):
        if not self.numberPad.isVisible():
            self.showShadowScreen()
            self.numberPad.start("", "thermal_chamber")

    def showShadowScreen(self):
        self.shadowScreen.show()
        self.shadowScreen.raise_()

    def closeShadowScreen(self):
        self.shadowScreen.hide()

    def on_reboot_button_clicked(self):
        self.showShadowScreen()
        ret = self.message.start("Mixware Screen", "Restart the printer?",
                                 buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.printer_reboot()
        self.closeShadowScreen()

    def on_header_clicked(self):
        if self._printer.information['led']['light'] == 0:
            self._printer.set_led_light(1)
        else:
            self._printer.set_led_light(0)

    def showEvent(self, a0: QShowEvent) -> None:
        self.stackedLayout.setCurrentIndex(0)
