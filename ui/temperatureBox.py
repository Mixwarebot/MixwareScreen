from qtCore import *
from ui.base.baseRound import BaseRoundWidget


class TemperatureBox(BaseRoundWidget):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.tips = QLabel()
        self.tips.setObjectName("title")
        self.tips.setFixedHeight(40)
        self.layout.addWidget(self.tips, 0, 0, 1, 2)

        self.leftLogo = QLabel()
        self.leftLogo.setObjectName("leftLogo")
        self.layout.addWidget(self.leftLogo, 2, 0, 2, 1)

        self.left = QPushButton()
        self.left.setObjectName("dataButton")
        self.left.setFixedHeight(72)
        self.layout.addWidget(self.left, 2, 1, 2, 1)

        self.rightLogo = QLabel()
        self.rightLogo.setObjectName("rightLogo")
        self.layout.addWidget(self.rightLogo, 4, 0, 2, 1)

        self.right = QPushButton()
        self.right.setObjectName("dataButton")
        self.right.setFixedHeight(72)
        self.layout.addWidget(self.right, 4, 1, 2, 1)

        self.bedLogo = QLabel()
        self.bedLogo.setObjectName("bedLogo")
        self.layout.addWidget(self.bedLogo, 6, 0, 2, 1)

        self.bed = QPushButton()
        self.bed.setObjectName("dataButton")
        self.bed.setFixedHeight(72)
        self.layout.addWidget(self.bed, 6, 1, 2, 1)

        self.chamberLogo = QLabel()
        self.chamberLogo.setObjectName("chamberLogo")
        self.layout.addWidget(self.chamberLogo, 8, 0, 2, 1)

        self.chamber = QPushButton()
        self.chamber.setObjectName("dataButton")
        self.chamber.setFixedHeight(72)
        self.layout.addWidget(self.chamber, 8, 1, 2, 1)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.tips.setText(self.tr("Temperature"))
        self.left.setText("-")
        self.right.setText("-")
        self.bed.setText("-")
        self.chamber.setText("-")

    @pyqtSlot()
    def on_update_printer_information(self):
        self.left.setText(self._printer.get_thermal('left'))
        self.right.setText(self._printer.get_thermal('right'))
        self.bed.setText(self._printer.get_thermal('bed'))
        self.chamber.setText(self._printer.get_thermal('chamber'))
