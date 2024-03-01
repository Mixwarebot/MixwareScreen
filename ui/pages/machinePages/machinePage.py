from qtCore import *
from ui.pages.machinePages.advancedPage import AdvancedPage
from ui.components.settingsButton import SettingsButton
from ui.components.settingsSwitch import SettingsSwitch


class MachinePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("machinePage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        # self.printMode = SettingsButton()
        # self.layout.addWidget(self.printMode)
        # self.heatingMode = SettingsButton()
        # self.layout.addWidget(self.heatingMode)
        # self.movementMode = SettingsButton()
        # self.layout.addWidget(self.movementMode)
        # self.filamentDetector = SettingsButton()
        # self.layout.addWidget(self.filamentDetector)
        # self.powerLossRecovery = SettingsButton()
        # self.layout.addWidget(self.powerLossRecovery)
        # self.thermalProtection = SettingsButton()
        # self.layout.addWidget(self.thermalProtection)

        self.run_out_switch = SettingsSwitch()
        self.run_out_switch.checkedChanged.connect(self.on_run_out_switch_value_changed)
        self.layout.addWidget(self.run_out_switch)

        self.plr_switch = SettingsSwitch()
        self.plr_switch.checkedChanged.connect(self.on_plr_switch_value_changed)
        self.layout.addWidget(self.plr_switch)

        self.advanced = SettingsButton()
        self.advanced.clicked.connect(self.goto_advanced_page)
        self.layout.addWidget(self.advanced)

        self.advancedPage = AdvancedPage(self._printer, self._parent)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()
        self.run_out_switch.setChecked(self._printer.get_run_out_enabled())
        self.plr_switch.setChecked(self._printer.config.enable_power_loss_recovery())

    def re_translate_ui(self):
        # self.printMode.setText(self.tr("Print Mode"))
        # self.heatingMode.setText(self.tr("Heating Mode"))
        # self.movementMode.setText(self.tr("Movement Mode"))
        # self.filamentDetector.setText(self.tr("Filament Detector"))
        # self.powerLossRecovery.setText(self.tr("Power Loss Recovery"))
        # self.thermalProtection.setText(self.tr("Thermal Protection"))
        self.run_out_switch.setText(self.tr("Filament Detection"))
        self.plr_switch.setText(self.tr("Power Loss Recovery"))
        self.advanced.setText(self.tr("Advanced Configuration"))

        # self.printMode._tips.setText("Normal")
        # self.heatingMode._tips.setText("Normal")
        # self.movementMode._tips.setText("Normal")

    def on_run_out_switch_value_changed(self, value):
        self._printer.set_run_out_enabled(value)

    def on_plr_switch_value_changed(self, value):
        self._printer.config.set_enable_power_loss_recovery(int(value))

    @pyqtSlot()
    def goto_advanced_page(self):
        self._parent.gotoPage(self.advancedPage, self.tr("Advanced Configuration"))
