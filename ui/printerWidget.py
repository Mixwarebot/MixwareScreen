import os

from qtCore import *
from ui.pages.base.basePrintWidget import BasePrintWidget
from ui.pages.printerPage import PrinterPage


class PrinterWidget(BasePrintWidget):
    updateTranslator = pyqtSignal(str)
    updateTheme = pyqtSignal(str)

    def __init__(self, printer, parent=None):
        super().__init__(printer, parent)
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.footer.previousButton.clicked.connect(self.goto_previous_page)

        self.printerPage = PrinterPage(self._printer, self)
        self.gotoPage(self.printerPage, self.header.title.text())
        self.footer.hide()

        self.power_loss_detect_timer = QTimer()
        self.power_loss_detect_timer.timeout.connect(self.on_power_loss_detect)

    def showEvent(self, a0: QShowEvent) -> None:
        if self._printer.is_connected():
            self._printer.write_gcode_command("D105\nD106")
            self.power_loss_detect_timer.start(1000)

    @pyqtSlot()
    def goto_previous_page(self):
        if self.stackedLayout.currentWidget() == self.printerPage.printFilePage \
                and self.printerPage.printFilePage.current_path != self.printerPage.printFilePage.root_path:
            self.printerPage.printFilePage.update_file(self.printerPage.printFilePage.current_path + "/..")
        else:
            self.gotoPreviousPage()

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.printerPage.temperatureWidget.left.setText(self._printer.get_thermal('left'))
        self.printerPage.temperatureWidget.right.setText(self._printer.get_thermal('right'))
        self.printerPage.temperatureWidget.bed.setText(self._printer.get_thermal('bed'))
        self.printerPage.temperatureWidget.chamber.setText(self._printer.get_thermal('chamber'))

    def on_power_loss_detect(self):
        self.power_loss_detect_timer.stop()
        if self._printer.is_connected():
            if self._printer.exists_power_loss() and self._printer.config.enable_power_loss_recovery():
                self.showShadowScreen()
                ret = self.message.start("Mixware Screen",
                                         self.tr("Power outage detected. Need to resume printing?"),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
                if ret == QMessageBox.Yes:
                    self._printer.print_resume()
                else:
                    os.remove(self._printer.power_loss_file)
                self.closeShadowScreen()
