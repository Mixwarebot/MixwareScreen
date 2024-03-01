from qtCore import *
from ui.components.settingsButton import SettingsButton


class JerkPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent

        self.setObjectName("jerkPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.jerk_x = SettingsButton()
        self.jerk_x.clicked.connect(self.on_jerk_x_clicked)
        self.layout.addWidget(self.jerk_x)

        self.jerk_y = SettingsButton()
        self.jerk_y.clicked.connect(self.on_jerk_y_clicked)
        self.layout.addWidget(self.jerk_y)

        self.jerk_z = SettingsButton()
        self.jerk_z.clicked.connect(self.on_jerk_z_clicked)
        self.layout.addWidget(self.jerk_z)

        self.jerk_e = SettingsButton()
        self.jerk_e.clicked.connect(self.on_jerk_e_clicked)
        self.layout.addWidget(self.jerk_e)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.jerk_x.setText(self.tr("X-Axis Jerk Limits"))
        self.jerk_y.setText(self.tr("Y-Axis Jerk Limits"))
        self.jerk_z.setText(self.tr("Z-Axis Jerk Limits"))
        self.jerk_e.setText(self.tr("E-Axis Jerk Limits"))

    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.jerk_x.setTips(f"{self._printer.information['motor']['jerk']['X']}")
        self.jerk_y.setTips(f"{self._printer.information['motor']['jerk']['Y']}")
        self.jerk_z.setTips(f"{self._printer.information['motor']['jerk']['Z']}")
        self.jerk_e.setTips(f"{self._printer.information['motor']['jerk']['E']}")

    @pyqtSlot()
    def on_jerk_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.jerk_x.text()}: {self.jerk_x.tips()}", "jerk_x")

    @pyqtSlot()
    def on_jerk_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.jerk_y.text()}: {self.jerk_y.tips()}", "jerk_y")

    @pyqtSlot()
    def on_jerk_z_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.jerk_z.text()}: {self.jerk_z.tips()}", "jerk_z")

    @pyqtSlot()
    def on_jerk_e_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.jerk_e.text()}: {self.jerk_e.tips()}", "jerk_e")
