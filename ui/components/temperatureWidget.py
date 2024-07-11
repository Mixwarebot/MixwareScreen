from qtCore import *
from ui.components.base.baseRound import BaseRoundWidget


class TemperatureWidget(BaseRoundWidget):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title = QLabel()
        self.title.setObjectName("title")
        self.title.setFixedHeight(40)
        self.layout.addWidget(self.title)

        self.content = QFrame()
        self.content_layout = QGridLayout(self.content)

        self.leftLogo = QLabel()
        self.leftLogo.setObjectName("leftLogo")
        self.content_layout.addWidget(self.leftLogo, 0, 0, 1, 1)

        self.left = QPushButton()
        self.left.setFixedHeight(72)
        self.content_layout.addWidget(self.left, 0, 1, 1, 1)

        self.rightLogo = QLabel()
        self.rightLogo.setObjectName("rightLogo")
        self.content_layout.addWidget(self.rightLogo, 2, 0, 1, 1)

        self.right = QPushButton()
        self.right.setFixedHeight(72)
        self.content_layout.addWidget(self.right, 2, 1, 1, 1)

        self.bedLogo = QLabel()
        self.bedLogo.setObjectName("bedLogo")
        self.content_layout.addWidget(self.bedLogo, 3, 0, 1, 1)

        self.bed = QPushButton()
        self.bed.setFixedHeight(72)
        self.content_layout.addWidget(self.bed, 3, 1, 1, 1)

        self.chamberLogo = QLabel()
        self.chamberLogo.setObjectName("chamberLogo")
        self.content_layout.addWidget(self.chamberLogo, 4, 0, 1, 1)

        self.chamber = QPushButton()
        self.chamber.setFixedHeight(72)
        self.content_layout.addWidget(self.chamber, 4, 1, 1, 1)
        self.layout.addWidget(self.content)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.title.setText(self.tr("Temperature"))
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
