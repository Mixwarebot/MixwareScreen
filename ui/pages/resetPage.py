import os

from qtCore import *
from ui.components.settingsButton import SettingsButton


class ResetPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("resetPage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 10)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.reset_printer = SettingsButton()
        self.reset_printer.clicked.connect(self.on_reset_printer_clicked)
        self.layout.addWidget(self.reset_printer)

        self.reset_ui = SettingsButton()
        self.reset_ui.clicked.connect(self.on_reset_ui_clicked)
        self.layout.addWidget(self.reset_ui)

        self.reset_all = SettingsButton()
        self.reset_all.clicked.connect(self.on_reset_all_clicked)
        self.layout.addWidget(self.reset_all)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.reset_printer.setText(self.tr("Restore Printer Factory Settings"))
        self.reset_ui.setText(self.tr("Reset Mixware Screen Settings"))
        self.reset_all.setText(self.tr("Reset All Settings"))

    def on_reset_printer_clicked(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.reset_printer.text(),
                                         self.tr("Click <Confirm> to restore\nthe printer to factory settings."),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.write_gcode_command('M502\nM500\nM503')
        self._parent.closeShadowScreen()

    @pyqtSlot()
    def on_reset_ui_clicked(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.reset_ui.text(),
                                         self.tr(
                                             "Click <Confirm> to\nreset Mixware Screen settings\nand Mixware Screen will restart."),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.config.reset_local_config()
            os.system('sudo clear && systemctl restart MixwareScreen')
        self._parent.closeShadowScreen()

    @pyqtSlot()
    def on_reset_all_clicked(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.reset_all.text(),
                                         self.tr(
                                             "Click <Confirm> to\nreset all settings and\nMixware Screen will restart."),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.write_gcode_command('M502\nM500')
            self._printer.config.reset_local_config()
            os.system('sudo clear && systemctl restart MixwareScreen')
        self._parent.closeShadowScreen()
