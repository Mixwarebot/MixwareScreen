from qtCore import *
from ui.settingsButton import SettingsButton


class StepPerUnitPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent

        self.setObjectName("stepPerUnitPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.step_x = SettingsButton()
        self.step_x.clicked.connect(self.on_step_x_clicked)
        self.layout.addWidget(self.step_x)

        self.step_y = SettingsButton()
        self.step_y.clicked.connect(self.on_step_y_clicked)
        self.layout.addWidget(self.step_y)

        self.step_z = SettingsButton()
        self.step_z.clicked.connect(self.on_step_z_clicked)
        self.layout.addWidget(self.step_z)

        self.step_e = SettingsButton()
        self.step_e.clicked.connect(self.on_step_e_clicked)
        self.layout.addWidget(self.step_e)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.step_x.setText(self.tr("X-Axis Step Per Unit"))
        self.step_y.setText(self.tr("Y-Axis Step Per Unit"))
        self.step_z.setText(self.tr("Z-Axis Step Per Unit"))
        self.step_e.setText(self.tr("E-Axis Step Per Unit"))

    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.step_x.setTips(f"{self._printer.information['motor']['stepPerUnit']['X']}")
        self.step_y.setTips(f"{self._printer.information['motor']['stepPerUnit']['Y']}")
        self.step_z.setTips(f"{self._printer.information['motor']['stepPerUnit']['Z']}")
        self.step_e.setTips(f"{self._printer.information['motor']['stepPerUnit']['E']}")

    @pyqtSlot()
    def on_step_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.step_x.text()}: {self.step_x.tips()}", "step_x")

    @pyqtSlot()
    def on_step_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.step_y.text()}: {self.step_y.tips()}", "step_y")

    @pyqtSlot()
    def on_step_z_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.step_z.text()}: {self.step_z.tips()}", "step_z")

    @pyqtSlot()
    def on_step_e_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.step_e.text()}: {self.step_e.tips()}", "step_e")
