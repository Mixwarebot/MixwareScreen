from qtCore import *
from ui.pages.machinePages.accelerationPage import AccelerationPage
from ui.pages.machinePages.feedRatePage import FeedRatePage
from ui.pages.machinePages.inputShaping import InputShapingPage
from ui.pages.machinePages.jerkPage import JerkPage
from ui.pages.machinePages.stepPage import StepPerUnitPage
from ui.pages.machinePages.tmcPage import TMCCurrentPage
from ui.components.settingsButton import SettingsButton


class AdvancedPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent

        self.setObjectName("advancedPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignTop)

        self.step_per_unit = SettingsButton()
        self.step_per_unit.clicked.connect(self.goto_step_per_unit_page)
        self.layout.addWidget(self.step_per_unit)

        self.feed_rate = SettingsButton()
        self.feed_rate.clicked.connect(self.goto_feed_rate_page)
        self.layout.addWidget(self.feed_rate)

        self.acceleration = SettingsButton()
        self.acceleration.clicked.connect(self.goto_acceleration_page)
        self.layout.addWidget(self.acceleration)

        self.jerk = SettingsButton()
        self.jerk.clicked.connect(self.goto_jerk_page)
        self.layout.addWidget(self.jerk)

        self.tmc_current = SettingsButton()
        self.tmc_current.clicked.connect(self.goto_tmc_current_page)
        self.layout.addWidget(self.tmc_current)

        # self.pid = SettingsButton()
        # self.layout.addWidget(self.pid)

        self.input_shaping = SettingsButton()
        self.input_shaping.clicked.connect(self.goto_input_shaping_page)
        self.layout.addWidget(self.input_shaping)

        self.linear_advance = SettingsButton()
        self.linear_advance.clicked.connect(self.on_linear_advance_clicked)
        self.layout.addWidget(self.linear_advance)

        self.save = SettingsButton()
        self.save.clicked.connect(self.on_save_clicked)
        self.layout.addWidget(self.save)

        self.restore_factory = SettingsButton()
        self.restore_factory.clicked.connect(self.on_restore_factory_clicked)
        self.layout.addWidget(self.restore_factory)

        self.stepPerUnitPage = StepPerUnitPage(self._printer, self._parent)
        self.feedRatePage = FeedRatePage(self._printer, self._parent)
        self.accelerationPage = AccelerationPage(self._printer, self._parent)
        self.jerkPage = JerkPage(self._printer, self._parent)
        self.tmcCurrentPage = TMCCurrentPage(self._printer, self._parent)
        self.inputShapingPage = InputShapingPage(self._printer, self._parent)

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.step_per_unit.setText(self.tr("Step Per Unit Settings"))
        self.feed_rate.setText(self.tr("Maximum Feed Rate Settings"))
        self.acceleration.setText(self.tr("Acceleration Settings"))
        self.jerk.setText(self.tr("Jerk Limits Settings"))
        self.tmc_current.setText(self.tr("TMC Current Settings"))
        self.input_shaping.setText(self.tr("Input Shaping Settings"))
        self.linear_advance.setText(self.tr("Linear Advance Settings"))
        # self.pid.setText(self.tr("P.I.D.  Settings"))
        self.restore_factory.setText(self.tr("Restore Printer Factory Settings"))
        self.save.setText(self.tr("Save Settings to Printer"))

    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.linear_advance.setTips(f"{self._printer.information['linearAdvance']}")

    @pyqtSlot()
    def goto_step_per_unit_page(self):
        self._parent.gotoPage(self.stepPerUnitPage, self.tr("Step Per Unit Settings"))

    @pyqtSlot()
    def goto_feed_rate_page(self):
        self._parent.gotoPage(self.feedRatePage, self.tr("Maximum Feed Rate Settings"))

    @pyqtSlot()
    def goto_acceleration_page(self):
        self._parent.gotoPage(self.accelerationPage, self.tr("Acceleration Settings"))

    @pyqtSlot()
    def goto_jerk_page(self):
        self._parent.gotoPage(self.jerkPage, self.tr("Jerk Limits Settings"))

    @pyqtSlot()
    def goto_tmc_current_page(self):
        self._parent.gotoPage(self.tmcCurrentPage, self.tr("TMC Current Settings"))

    @pyqtSlot()
    def goto_input_shaping_page(self):
        self._parent.gotoPage(self.inputShapingPage, self.tr("Input Shaping Settings"))

    @pyqtSlot()
    def on_linear_advance_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"{self.linear_advance.text()}: {self.linear_advance.tips()}",
                                         "linear_advance")

    @pyqtSlot()
    def on_restore_factory_clicked(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.restore_factory.text(),
                                         self.tr("Click <Confirm> to restore\nthe printer to factory settings."),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.write_gcode_command('M502\nM500\nM503')
        self._parent.closeShadowScreen()

    @pyqtSlot()
    def on_save_clicked(self):
        self._parent.showShadowScreen()
        ret = self._parent.message.start(self.save.text(), self.tr("Click <Confirm> to save."),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.write_gcode_command('M500')
        self._parent.closeShadowScreen()
