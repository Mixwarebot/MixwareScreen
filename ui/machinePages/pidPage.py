from qtCore import *
from ui.settingsButton import SettingsButton


class PIDPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent

        self.setObjectName("pidPage")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        pass

    def on_update_printer_information(self):
        if not self.isVisible():
            return
