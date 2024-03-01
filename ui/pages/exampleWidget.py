from qtCore import *


class ExampleWidget(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self._parent = parent

        self.setObjectName("exampleWidget")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 10)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.layout.addWidget(self.frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        pass

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
