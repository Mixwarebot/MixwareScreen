from qtCore import *
from ui.components.base.baseLine import BaseHLine


class ThermalWidget(QFrame):
    thermalChanged = pyqtSignal()

    def __init__(self, printer, parent, show_line=True, show_bed=False, show_chamber=False):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self._parent = parent
        self._line_count = 0
        self._show_line = show_line
        self._show_bed = show_bed
        self._show_chamber = show_chamber

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._left_logo = QLabel()
        self._left_logo.setObjectName("leftLogo")
        self._layout.addWidget(self._left_logo, self._line_count, 0, 1, 1)
        self._left_button = QPushButton()
        self._left_button.setFixedHeight(64)
        self._left_button.clicked.connect(self.on_left_button_clicked)
        self._layout.addWidget(self._left_button, self._line_count, 1, 1, 1)

        self.add_line()

        self._line_count += 1
        self._right_logo = QLabel()
        self._right_logo.setObjectName("rightLogo")
        self._layout.addWidget(self._right_logo, self._line_count, 0, 1, 1)
        self._right_button = QPushButton()
        self._right_button.setFixedHeight(64)
        self._right_button.clicked.connect(self.on_right_button_clicked)
        self._layout.addWidget(self._right_button, self._line_count, 1, 1, 1)

        if self._show_bed:
            self.add_line()
            self._line_count += 1
            self._bed_logo = QLabel()
            self._bed_logo.setObjectName("bedLogo")
            self._layout.addWidget(self._bed_logo, self._line_count, 0, 1, 1)
            self._bed_button = QPushButton()
            self._bed_button.setFixedHeight(64)
            self._bed_button.clicked.connect(self.on_bed_button_clicked)
            self._layout.addWidget(self._bed_button, self._line_count, 1, 1, 1)

        if self._show_chamber:
            self.add_line()
            self._line_count += 1
            self._chamber_logo = QLabel()
            self._chamber_logo.setObjectName("chamberLogo")
            self._layout.addWidget(self._chamber_logo, self._line_count, 0, 1, 1)
            self._chamber_button = QPushButton()
            self._chamber_button.setFixedHeight(64)
            self._chamber_button.clicked.connect(self.on_chamber_button_clicked)
            self._layout.addWidget(self._chamber_button, self._line_count, 1, 1, 1)

        self.add_line()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self._left_button.setText("-")
        self._right_button.setText("-")
        if self._show_bed: self._bed_button.setText("-")
        if self._show_chamber: self._chamber_button.setText("-")

    @pyqtSlot()
    def on_update_printer_information(self):
        if self.isVisible():
            self._left_button.setText(self._printer.get_thermal('left'))
            self._right_button.setText(self._printer.get_thermal('right'))
            if self._show_bed: self._bed_button.setText(self._printer.get_thermal('bed'))
            if self._show_chamber: self._chamber_button.setText(self._printer.get_thermal('chamber'))

    def on_left_button_clicked(self):
        self._parent.open_thermal_left_numberPad()
        self.thermalChanged.emit()

    def on_right_button_clicked(self):
        self._parent.open_thermal_right_numberPad()
        self.thermalChanged.emit()

    def on_bed_button_clicked(self):
        self._parent.open_thermal_bed_numberPad()
        self.thermalChanged.emit()

    def on_chamber_button_clicked(self):
        self._parent.open_thermal_chamber_numberPad()
        self.thermalChanged.emit()

    def add_line(self):
        if self._show_line:
            self._line_count += 1
            self._layout.addWidget(BaseHLine(), self._line_count, 0, 1, 2)
