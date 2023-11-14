from qtCore import *
from ui.base.basePrintWidget import BasePrintWidget
from ui.printerPage import PrinterPage


class PrinterWidget(BasePrintWidget):
    updateTranslator = pyqtSignal(str)
    updateTheme = pyqtSignal(str)
    def __init__(self, printer, parent=None):
        super().__init__(printer, parent)
        self._printer = printer

        self.printerPage = PrinterPage(self._printer, self)

        self.initForm()
        self.initConnect()

    def initForm(self):
        self.gotoPage(self.printerPage, self.header.title.text())
        self.footer.hide()

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)
        self.footer.previousButton.clicked.connect(self.goto_previous_page)

    @pyqtSlot()
    def goto_previous_page(self):
        if self.stackedLayout.currentWidget() == self.printerPage.printFilePage and self.printerPage.printFilePage.current_path != self.printerPage.printFilePage.root_path:
            self.printerPage.printFilePage.update_file(self.printerPage.printFilePage.current_path + "/..")
        else:
            self.gotoPreviousPage()

    @pyqtSlot()
    def onUpdatePrinterInformation(self):
        self.printerPage.temperatureWidget.left.setText(self._printer.get_thermal('left'))
        self.printerPage.temperatureWidget.right.setText(self._printer.get_thermal('right'))
        self.printerPage.temperatureWidget.bed.setText(self._printer.get_thermal('bed'))
        self.printerPage.temperatureWidget.chamber.setText(self._printer.get_thermal('chamber'))

    @pyqtSlot()
    def on_redetect_button_clicked(self):
        self.showShadowScreen()
        ret = self.message.start("Mixware Screen", "on_redetect_button_clicked?", buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.write_gcode_command('G28\nD28\nG29\nM500')
        self.closeShadowScreen()

    def showEvent(self, QShowEvent) -> None:
        self._printer.write_gcode_command("D105\nD106")

