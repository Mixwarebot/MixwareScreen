from qtCore import *
from ui.machinePages.advancedPage import AdvancedPage
from ui.settingsButton import SettingsButton


class MachinePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("machinePage")

        self.printMode = SettingsButton()
        self.heatingMode = SettingsButton()
        self.movementMode = SettingsButton()
        self.filamentDetector = SettingsButton()
        self.powerLossRecovery = SettingsButton()
        self.thermalProtection = SettingsButton()
        self.advanced = SettingsButton()

        self.advancedPage = AdvancedPage(self._printer, self._parent)

        self.initForm()
        self.initLayout()
        self.initConnect()

    def initForm(self):

        self.printMode.setText(self.tr("Print Mode"))
        self.heatingMode.setText(self.tr("Heating Mode"))
        self.movementMode.setText(self.tr("Movement Mode"))
        self.filamentDetector.setText(self.tr("Filament Detector"))
        self.powerLossRecovery.setText(self.tr("Power Loss Recovery"))
        self.thermalProtection.setText(self.tr("Thermal Protection"))
        self.advanced.setText(self.tr("Advanced Configuration"))

        self.printMode._tips.setText("Normal")
        self.heatingMode._tips.setText("Normal")
        self.movementMode._tips.setText("Normal")

    def initLayout(self):
        layout = QVBoxLayout(self)
        # layout.addWidget(self.printMode)
        # layout.addWidget(self.heatingMode)
        # layout.addWidget(self.movementMode)
        # layout.addWidget(self.filamentDetector)
        # layout.addWidget(self.powerLossRecovery)
        # layout.addWidget(self.thermalProtection)
        layout.addWidget(self.advanced)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)

    def initConnect(self):
        self.advanced.clicked.connect(self.gotoAdvancedPage)

    @pyqtSlot()
    def gotoAdvancedPage(self):
        # self._printer.write_gcode_command("D105")
        self._parent.gotoPage(self.advancedPage, self.tr("Advanced Configuration"))