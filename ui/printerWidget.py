from qtCore import *
from ui.base.basePrintWidget import BasePrintWidget
from ui.printerPage import PrinterPage


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

    def showEvent(self, a0: QShowEvent) -> None:
        self._printer.write_gcode_command("D105\nD106")

    @pyqtSlot()
    def goto_previous_page(self):
        if self.stackedLayout.currentWidget() == self.printerPage.printFilePage \
                and self.printerPage.printFilePage.current_path != self.printerPage.printFilePage.root_path:
            self.printerPage.printFilePage.update_file(self.printerPage.printFilePage.current_path + "/..")
        else:
            self.gotoPreviousPage()

    @pyqtSlot()
    def on_update_printer_information(self):
        self.printerPage.temperatureWidget.left.setText(self._printer.get_thermal('left'))
        self.printerPage.temperatureWidget.right.setText(self._printer.get_thermal('right'))
        self.printerPage.temperatureWidget.bed.setText(self._printer.get_thermal('bed'))
        self.printerPage.temperatureWidget.chamber.setText(self._printer.get_thermal('chamber'))
