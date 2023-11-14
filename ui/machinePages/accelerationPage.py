from qtCore import *
from ui.settingsButton import SettingsButton


class AccelerationPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("accelerationPage")

        self.acceleration_x = SettingsButton()
        self.acceleration_y = SettingsButton()
        self.acceleration_z = SettingsButton()
        self.acceleration_e = SettingsButton()
        self.acceleration_print = SettingsButton()
        self.acceleration_retract = SettingsButton()
        self.acceleration_travel = SettingsButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.reTranslateUi()

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.acceleration_x)
        layout.addWidget(self.acceleration_y)
        layout.addWidget(self.acceleration_z)
        layout.addWidget(self.acceleration_e)
        layout.addWidget(self.acceleration_print)
        layout.addWidget(self.acceleration_retract)
        layout.addWidget(self.acceleration_travel)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)
        self.acceleration_x.clicked.connect(self.on_acceleration_x_clicked)
        self.acceleration_y.clicked.connect(self.on_acceleration_y_clicked)
        self.acceleration_z.clicked.connect(self.on_acceleration_z_clicked)
        self.acceleration_e.clicked.connect(self.on_acceleration_e_clicked)
        self.acceleration_print.clicked.connect(self.on_acceleration_print_clicked)
        self.acceleration_retract.clicked.connect(self.on_acceleration_retract_clicked)
        self.acceleration_travel.clicked.connect(self.on_acceleration_travel_clicked)

    @pyqtSlot()
    def on_acceleration_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_x.text()}: {self.acceleration_x.tips()}", "acceleration_x")

    @pyqtSlot()
    def on_acceleration_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_y.text()}: {self.acceleration_y.tips()}", "acceleration_y")

    @pyqtSlot()
    def on_acceleration_z_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_z.text()}: {self.acceleration_z.tips()}", "acceleration_z")

    @pyqtSlot()
    def on_acceleration_e_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_e.text()}: {self.acceleration_e.tips()}", "acceleration_e")

    @pyqtSlot()
    def on_acceleration_print_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_print.text()}: {self.acceleration_print.tips()}", "acceleration_print")

    @pyqtSlot()
    def on_acceleration_retract_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_retract.text()}: {self.acceleration_retract.tips()}", "acceleration_retract")

    @pyqtSlot()
    def on_acceleration_travel_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.acceleration_travel.text()}: {self.acceleration_travel.tips()}", "acceleration_travel")

    def onUpdatePrinterInformation(self):
        self.reTranslateUi()

    def reTranslateUi(self):
        self.acceleration_x.setText(self.tr("X-Axis Acceleration"))
        self.acceleration_y.setText(self.tr("Y-Axis Acceleration"))
        self.acceleration_z.setText(self.tr("Z-Axis Acceleration"))
        self.acceleration_e.setText(self.tr("E-Axis Acceleration"))
        self.acceleration_print.setText(self.tr("Acceleration"))
        self.acceleration_retract.setText(self.tr("Retracts Acceleration"))
        self.acceleration_travel.setText(self.tr("Travel Acceleration"))

        self.acceleration_x.setTips(f"{self._printer.information['motor']['maxAcceleration']['X']}")
        self.acceleration_y.setTips(f"{self._printer.information['motor']['maxAcceleration']['Y']}")
        self.acceleration_z.setTips(f"{self._printer.information['motor']['maxAcceleration']['Z']}")
        self.acceleration_e.setTips(f"{self._printer.information['motor']['maxAcceleration']['E']}")
        self.acceleration_print.setTips(f"{self._printer.information['motor']['acceleration']}")
        self.acceleration_retract.setTips(f"{self._printer.information['motor']['accelerationRetract']}")
        self.acceleration_travel.setTips(f"{self._printer.information['motor']['accelerationTravel']}")

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()