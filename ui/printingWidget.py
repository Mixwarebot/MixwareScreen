import os

from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.pages.base.basePrintWidget import BasePrintWidget
from ui.pages.filamentPage import FilamentPage
from ui.pages.levelPages.babyStepPad import BabyStepPad
from ui.components.printDoneDialog import PrintDoneDialog
from ui.pages.printingPage import PrintingPage
from ui.components.runoutPad import RunOutPad


class PrintingWidget(BasePrintWidget):
    print_done = pyqtSignal()

    def __init__(self, printer, parent=None):
        super().__init__(printer, parent)
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)

        self.printingPage = PrintingPage()
        self.printingPage.setObjectName("printingPage")
        self.printingPage.print_progress_bar.valueChanged.connect(self.on_print_progress_bar_value_changed)
        self.printingPage.pause_print_button.clicked.connect(self.on_pause_button_clicked)
        self.printingPage.stop_print_button.clicked.connect(self.on_stop_button_clicked)
        self.printingPage.baby_step_button.clicked.connect(self.on_baby_step_button_clicked)
        self.printingPage.thermal_left_button.clicked.connect(self.open_thermal_left_numberPad)
        self.printingPage.thermal_right_button.clicked.connect(self.open_thermal_right_numberPad)
        self.printingPage.thermal_bed_button.clicked.connect(self.open_thermal_bed_numberPad)
        self.printingPage.thermal_chamber_button.clicked.connect(self.open_thermal_chamber_numberPad)
        self.printingPage.fan_left_button.clicked.connect(self.on_fan_left_button_clicked)
        self.printingPage.fan_right_button.clicked.connect(self.on_fan_right_button_clicked)
        self.printingPage.fan_exhaust_button.clicked.connect(self.on_fan_exhaust_button_clicked)
        self.printingPage.speed_print_button.clicked.connect(self.on_speed_print_button_clicked)
        self.printingPage.speed_flow_button.clicked.connect(self.on_speed_flow_button_clicked)
        self.printingPage.filament_detector_enabled.checkedChanged.connect(self.on_run_out_switch_value_changed)
        self.printingPage.filament_changed_button.clicked.connect(self.on_filament_changed_button_clicked)
        # self.stackedLayout.addWidget(self.printingPage)
        self.gotoPage(self.printingPage, self.header.title.text())
        self.footer.previousButton.clicked.connect(self.gotoPreviousPage)
        self.footer.hide()

        self.babyStepPad = BabyStepPad(self._printer)
        self.babyStepPad.rejected.connect(self.closeShadowScreen)
        self.runOutPad = RunOutPad(self._printer)
        self.printDoneDialog = PrintDoneDialog(self._printer)
        self.filament_page = FilamentPage(self._printer, self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimerTriggered)

        self.timerHours = 0
        self.timerMinutes = 0
        self.timerSeconds = 0
        self.reset_time()
        self.timer.start(1000)

    def showEvent(self, a0: QShowEvent) -> None:
        self._printer.pull_position = True
        self.printingPage.filament_detector_enabled.set_checked(self._printer.get_run_out_enabled())
        self.update_pause_print_button_style()

    def hideEvent(self, a0: QShowEvent) -> None:
        self._printer.pull_position = False

    def onButtonClicked(self):  # test
        filepath, _ = QFileDialog.getOpenFileName(None, "pic", ".", "*.png")
        picture = QPixmap()
        picture.load(filepath)
        self.printingPage.file_image.setPixmap(picture)

    def on_motor_y_button_clicked(self):
        self.runOutPad.start()

    def on_baby_step_button_clicked(self):
        if not self.babyStepPad.isVisible():
            self.showShadowScreen()
            self.babyStepPad.exec()

    def on_fan_left_button_clicked(self):
        if not self.numberPad.isVisible():
            message = self.tr("Left Model Fan Speed: {}%").format(int(self._printer.get_fan_speed('left')) * 100)
            self.showShadowScreen()
            self.numberPad.start(message, "fan_left")

    def on_fan_right_button_clicked(self):
        if not self.numberPad.isVisible():
            message = self.tr("Right Model Fan Speed: {}%").format(int(self._printer.get_fan_speed('right')) * 100)
            self.showShadowScreen()
            self.numberPad.start(message, "fan_right")

    def on_fan_exhaust_button_clicked(self):
        if not self.numberPad.isVisible():
            message = self.tr("Exhaust Fan Speed: {}%").format(int(self._printer.get_fan_speed('exhaust')) * 100)
            self.showShadowScreen()
            self.numberPad.start(message, "fan_exhaust")

    def on_speed_print_button_clicked(self):
        if not self.numberPad.isVisible():
            message = self.tr("Print Feed Rate: {}%").format(self._printer.get_print_feed_rate())
            self.showShadowScreen()
            self.numberPad.start(message, "print_feed_rate")

    def on_speed_flow_button_clicked(self):
        if not self.numberPad.isVisible():
            message = self.tr("Print Flow: {}%").format(self._printer.get_print_flow())
            self.showShadowScreen()
            self.numberPad.start(message, "print_flow")

    def set_file_name(self, path):
        file_info = QFileInfo(path)
        self.printingPage.file_name.setText(file_info.fileName())

        image = f'{file_info.absolutePath()}/.thumbs/{file_info.completeBaseName()}.png'
        if os.path.isfile(image):
            self.printingPage.file_image.setPixmap(QPixmap(image).scaledToWidth(360))
        else:
            self.printingPage.file_image.setPixmap(QPixmap("resource/image/hyper-x").scaledToWidth(360))

    def reset_time(self):
        self.timerSeconds = 0
        self.timerMinutes = 0
        self.timerHours = 0
        self.printingPage.print_time.setText(f"{self.timerHours}:{self.timerMinutes:02}:{self.timerSeconds:02}")

    def update_time(self):
        self.timerSeconds += 1
        if self.timerSeconds == 60:
            self.timerMinutes += 1
            self.timerSeconds = 0
        if self.timerMinutes == 60:
            self.timerHours += 1
            self.timerMinutes = 0

    def on_print_progress_bar_value_changed(self):
        self.printingPage.print_progress_label.setText(self.printingPage.print_progress_bar.text())

    def onTimerTriggered(self):
        if self._printer.is_printing():
            if not self._printer.is_paused():
                self.update_time()
                self.printingPage.print_time.setText(f"{self.timerHours}:{self.timerMinutes:02}:{self.timerSeconds:02}")
                self.printingPage.print_progress_bar.setValue(int(self._printer.print_progress() * 100))
                if self._printer.config.enable_power_loss_recovery():
                    self._printer.print_backup()

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.printingPage.thermal_left_button.setText(self._printer.get_thermal('left'))
        self.printingPage.thermal_right_button.setText(self._printer.get_thermal('right'))
        self.printingPage.thermal_bed_button.setText(self._printer.get_thermal('bed'))
        self.printingPage.thermal_chamber_button.setText(self._printer.get_thermal('chamber'))

        self.printingPage.motor_z.setText(str(self._printer.get_position('Z')))

        self.printingPage.fan_cool_left.setText(str(int(self._printer.get_fan_speed('leftCool') * 100)) + "%")
        self.printingPage.fan_cool_right.setText(str(int(self._printer.get_fan_speed('rightCool') * 100)) + "%")
        self.printingPage.fan_chamber.setText(str(int(self._printer.get_fan_speed('chamber') * 100)) + "%")
        self.printingPage.fan_left_button.setText(str(int(self._printer.get_fan_speed('left') * 100)) + "%")
        self.printingPage.fan_right_button.setText(str(int(self._printer.get_fan_speed('right') * 100)) + "%")
        self.printingPage.fan_exhaust_button.setText(str(int(self._printer.get_fan_speed('exhaust') * 100)) + "%")

        self.printingPage.speed_print_button.setText(f'{self._printer.get_print_feed_rate()}%')
        self.printingPage.speed_flow_button.setText(f'{self._printer.get_print_flow()}%')

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, status):
        if not self.isVisible():
            return
        if status == MixwareScreenPrinterStatus.PRINTER_PRINT_FINISHED:
            self.on_print_finished()
        elif status == MixwareScreenPrinterStatus.PRINTER_RUN_OUT:
            if self._printer.is_printing():
                if not self._printer.is_paused():
                    if not self.runOutPad.isVisible():
                        self.showShadowScreen()
                        self.print_pause()
                        self._printer.write_gcode_commands("G1 Y20 F8400")
                        self.runOutPad.start()
                        self.closeShadowScreen()
                        self.update_pause_print_button_style()

    def update_pause_print_button_style(self):
        if self._printer.is_paused():
            update_style(self.printingPage.pause_print_button, "resumePrintButton")
        else:
            update_style(self.printingPage.pause_print_button, "pausePrintButton")

    def print_resume(self):
        self._printer.print_resume()
        self.update_pause_print_button_style()

    def print_pause(self):
        self._printer.print_pause()
        self.update_pause_print_button_style()

    def on_pause_button_clicked(self):
        if self._printer.is_printing():
            self.showShadowScreen()
            # paused => printing
            if self._printer.is_paused():
                ret = self.message.start("Mixware Screen", self.tr("Resume Printing?"),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
                if ret == QMessageBox.Yes:
                    self.print_resume()
            # printing => pause
            else:
                ret = self.message.start("Mixware Screen", self.tr("Pause Printing?"),
                                         buttons=QMessageBox.Yes | QMessageBox.Cancel)
                if ret == QMessageBox.Yes:
                    self.print_pause()
            self.closeShadowScreen()

    def on_stop_button_clicked(self):
        self.showShadowScreen()
        ret = self.message.start("Mixware Screen", self.tr("Stop Printing?"),
                                 buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            self._printer.print_stop()
        self.closeShadowScreen()

    def on_print_finished(self):
        self.showShadowScreen()
        ret = self.printDoneDialog.start("Mixware Screen", self.tr("Print Done.\nPrint time: {}").format(
            self.printingPage.print_time.text()))
        if ret == QMessageBox.Yes:
            self.reset_time()
            self._printer.print_again()
        elif ret == QMessageBox.Cancel:
            self.print_done.emit()
        self.closeShadowScreen()

    def on_run_out_switch_value_changed(self, value):
        self._printer.set_run_out_enabled(value)

    def on_filament_changed_button_clicked(self):
        self.showShadowScreen()
        ret = self.message.start("Mixware Screen", self.tr("Replacing the filament will pause printing."),
                                 buttons=QMessageBox.Yes | QMessageBox.Cancel)
        if ret == QMessageBox.Yes:
            if self._printer.is_printing():
                self._printer.print_pause()
            self.filament_page.backup_target()
            self.gotoPage(self.filament_page, self.tr("Replace Filament"))
        self.closeShadowScreen()
