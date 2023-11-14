from qtCore import *
from ui.base.baseRound import BaseRoundWidget


class PrinterTemperatureWidget(BaseRoundWidget):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer

        self.tips = QLabel()
        self.tips.setFixedHeight(40)
        self.leftLogo = QLabel()
        self.rightLogo = QLabel()
        self.bedLogo = QLabel()
        self.chamberLogo = QLabel()
        self.left = QPushButton()
        self.right = QPushButton()
        self.bed = QPushButton()
        self.chamber = QPushButton()
        self.left.setFixedHeight(64)
        self.right.setFixedHeight(64)
        self.bed.setFixedHeight(64)
        self.chamber.setFixedHeight(64)

        self.tips.setObjectName("title")
        self.leftLogo.setObjectName("leftLogo")
        self.rightLogo.setObjectName("rightLogo")
        self.bedLogo.setObjectName("bedLogo")
        self.chamberLogo.setObjectName("chamberLogo")
        self.left.setObjectName("dataButton")
        self.right.setObjectName("dataButton")
        self.bed.setObjectName("dataButton")
        self.chamber.setObjectName("dataButton")

        self.tips.setText(self.tr("Temperature"))
        self.left.setText("0")
        self.right.setText("0")
        self.bed.setText("0")
        self.chamber.setText("0")

        layout = QGridLayout()
        layout.addWidget(self.tips, 0, 0, 1, 2)
        layout.addWidget(self.leftLogo, 2, 0, 2, 1)
        layout.addWidget(self.left, 2, 1, 2, 1)
        layout.addWidget(self.rightLogo, 4, 0, 2, 1)
        layout.addWidget(self.right, 4, 1, 2, 1)
        layout.addWidget(self.bedLogo, 6, 0, 2, 1)
        layout.addWidget(self.bed, 6, 1, 2, 1)
        layout.addWidget(self.chamberLogo, 8, 0, 2, 1)
        layout.addWidget(self.chamber, 8, 1, 2, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)

    @pyqtSlot()
    def onUpdatePrinterInformation(self):
        self.left.setText(self._printer.get_thermal('left'))
        self.right.setText(self._printer.get_thermal('right'))
        self.bed.setText(self._printer.get_thermal('bed'))
        self.chamber.setText(self._printer.get_thermal('chamber'))