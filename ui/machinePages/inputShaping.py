from qtCore import *
from ui.settingsButton import SettingsButton


class InputShapingPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("inputShapingPage")

        self.frequency_x = SettingsButton()
        self.frequency_y = SettingsButton()
        self.damping_x = SettingsButton()
        self.damping_y = SettingsButton()

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):
        self.reTranslateUi()

    def initLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.frequency_x)
        layout.addWidget(self.damping_x)
        layout.addWidget(self.frequency_y)
        layout.addWidget(self.damping_y)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)
        self.frequency_x.clicked.connect(self.on_frequency_x_clicked)
        self.frequency_y.clicked.connect(self.on_frequency_y_clicked)
        self.damping_x.clicked.connect(self.on_damping_x_clicked)
        self.damping_y.clicked.connect(self.on_damping_y_clicked)

    @pyqtSlot()
    def on_frequency_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.frequency_x.text()}: {self.frequency_x.tips()}", "frequency_x")

    @pyqtSlot()
    def on_frequency_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.frequency_y.text()}: {self.frequency_y.tips()}", "frequency_y")

    @pyqtSlot()
    def on_damping_x_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.damping_x.text()}: {self.damping_x.tips()}", "damping_x")

    @pyqtSlot()
    def on_damping_y_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.damping_y.text()}: {self.damping_y.tips()}", "damping_y")

    def onUpdatePrinterInformation(self):
        self.reTranslateUi()

    def reTranslateUi(self):
        self.frequency_x.setText(self.tr("X-Axis Frequency"))
        self.frequency_y.setText(self.tr("Y-Axis Frequency"))
        self.damping_x.setText(self.tr("X-Axis Damping"))
        self.damping_y.setText(self.tr("Y-Axis Damping"))

        self.frequency_x.setTips(f"{self._printer.information['inputShaping']['X']['frequency']}")
        self.frequency_y.setTips(f"{self._printer.information['inputShaping']['Y']['frequency']}")
        self.damping_x.setTips(f"{self._printer.information['inputShaping']['X']['damping']}")
        self.damping_y.setTips(f"{self._printer.information['inputShaping']['Y']['damping']}")

    def showEvent(self, a0: QShowEvent) -> None:
        self.reTranslateUi()
