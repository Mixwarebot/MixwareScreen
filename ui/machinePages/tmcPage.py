from qtCore import *
from ui.settingsButton import SettingsButton


class TMCCurrentPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("tmcCurrentPage")

        self.current_x = SettingsButton()
        self.current_x2 = SettingsButton()
        self.current_y = SettingsButton()
        self.current_z = SettingsButton()
        self.current_z2 = SettingsButton()
        self.current_e = SettingsButton()
        self.current_e2 = SettingsButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.reTranslateUi()

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.current_x)
        layout.addWidget(self.current_x2)
        layout.addWidget(self.current_y)
        layout.addWidget(self.current_z)
        layout.addWidget(self.current_z2)
        layout.addWidget(self.current_e)
        layout.addWidget(self.current_e2)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)
        self.current_x.clicked.connect(self.on_current_x_clicked)
        self.current_x2.clicked.connect(self.on_current_x2_clicked)
        self.current_y.clicked.connect(self.on_current_y_clicked)
        self.current_z.clicked.connect(self.on_current_z_clicked)
        self.current_z2.clicked.connect(self.on_current_z2_clicked)
        self.current_e.clicked.connect(self.on_current_e_clicked)
        self.current_e2.clicked.connect(self.on_current_e2_clicked)

    @pyqtSlot()
    def on_current_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_x.text()}: {self.current_x.tips()}", "current_x")

    @pyqtSlot()
    def on_current_x2_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_x2.text()}: {self.current_x2.tips()}", "current_x2")

    @pyqtSlot()
    def on_current_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_y.text()}: {self.current_y.tips()}", "current_y")

    @pyqtSlot()
    def on_current_z_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_z.text()}: {self.current_z.tips()}", "current_z")

    @pyqtSlot()
    def on_current_z2_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_z2.text()}: {self.current_z2.tips()}", "current_z2")

    @pyqtSlot()
    def on_current_e_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_e.text()}: {self.current_e.tips()}", "current_e")

    @pyqtSlot()
    def on_current_e2_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.current_e2.text()}: {self.current_e2.tips()}", "current_e2")

    def onUpdatePrinterInformation(self):
        self.reTranslateUi()

    def reTranslateUi(self):
        self.current_x.setText(self.tr("X-Axis TMC Current"))
        self.current_x2.setText(self.tr("X2-Axis TMC Current"))
        self.current_y.setText(self.tr("Y-Axis TMC Current"))
        self.current_z.setText(self.tr("Z-Axis TMC Current"))
        self.current_z2.setText(self.tr("Z2-Axis TMC Current"))
        self.current_e.setText(self.tr("E-Axis TMC Current"))
        self.current_e2.setText(self.tr("E2-Axis TMC Current"))

        self.current_x.setTips(f"{self._printer.information['motor']['drivers']['current']['X']}")
        self.current_x2.setTips(f"{self._printer.information['motor']['drivers']['current']['X2']}")
        self.current_y.setTips(f"{self._printer.information['motor']['drivers']['current']['Y']}")
        self.current_z.setTips(f"{self._printer.information['motor']['drivers']['current']['Z']}")
        self.current_z2.setTips(f"{self._printer.information['motor']['drivers']['current']['Z2']}")
        self.current_e.setTips(f"{self._printer.information['motor']['drivers']['current']['E']}")
        self.current_e2.setTips(f"{self._printer.information['motor']['drivers']['current']['E1']}")

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()
