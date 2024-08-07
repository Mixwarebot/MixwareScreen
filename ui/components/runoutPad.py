import platform
from enum import Enum, auto

from qtCore import *
from ui.components.base.baseLine import BaseHLine, BaseVLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.base.baseRound import BaseRoundDialog


class RunOutStatus(Enum):
    RUNOUT_NULL = auto()
    RUNOUT_UNLOAD = auto()
    RUNOUT_CLEAN = auto()
    RUNOUT_HEAT = auto()
    RUNOUT_LOAD = auto()
    RUNOUT_EXIT = auto()


class RunOutPad(BaseRoundDialog):
    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._width = self._printer.config.get_width()
        self._height = self._printer.config.get_height()
        self.message_print = ""
        self.message_unload = ""
        self.message_clean = ""
        self.message_load = ""

        self.status = RunOutStatus.RUNOUT_NULL

        self.resize(self._width - 40, self._height / 3)
        self.move((self._width - self.width()) / 2, (self._height - self.height()) / 2)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.frame = QFrame()
        self.frame.setObjectName("frameBox")
        self.frame.setStyleSheet("QFrame#frameBox { border: none; }")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        # self.frame_layout.setAlignment(Qt.AlignTop)

        self.title_frame = QFrame()
        self.title_frame.setFixedHeight(40)
        self.title_frame.setObjectName("title")
        title_frame_layout = QHBoxLayout(self.title_frame)
        title_frame_layout.setContentsMargins(0, 0, 0, 0)
        title_frame_layout.setSpacing(0)
        self.title_label = QLabel()
        self.title_label.setFixedHeight(40)
        title_frame_layout.addWidget(self.title_label)
        self.title_close_button = BasePushButton()
        self.title_close_button.setObjectName("closeButton")
        self.title_close_button.setFlat(True)
        self.title_close_button.setFixedSize(40, 40)
        self.title_close_button.clicked.connect(self.on_close_button_clicked)
        title_frame_layout.addWidget(self.title_close_button)
        self.frame_layout.addWidget(self.title_frame)

        self.body = QFrame(self)
        self.body_frame_layout = QVBoxLayout(self.body)
        self.body_frame_layout.setContentsMargins(10, 20, 10, 10)
        self.body_frame_layout.setSpacing(0)
        self.message_label = QLabel()
        self.message_label.setObjectName("numberPadInformationLabel")
        self.message_label.setFixedWidth(self.width() - 20)
        self.message_label.setAlignment(Qt.AlignTop)
        self.message_label.setWordWrap(True)
        self.body_frame_layout.addWidget(self.message_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.body_frame_layout.addWidget(self.progress_bar)
        self.frame_layout.addWidget(self.body)
        self.frame_layout.addWidget(BaseHLine())

        self.footer = QFrame(self)
        self.footer.setFixedHeight(64)
        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(0)
        self.load_again_button = BasePushButton()
        self.load_again_button.clicked.connect(self.start_load)
        self.footer_layout.addWidget(self.load_again_button)
        self.footer_line = BaseVLine()
        self.footer_line.setFixedHeight(48)
        self.footer_layout.addWidget(self.footer_line)
        self.next_button = BasePushButton()
        self.next_button.clicked.connect(self.on_next_button_clicked)
        self.footer_layout.addWidget(self.next_button)
        self.frame_layout.addWidget(self.footer)
        self.layout.addWidget(self.frame)

        self.working_timer = QTimer()
        self.working_timer.timeout.connect(self.on_working_timer_timeout)
        self.working_progress = 0

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.title_close_button.setText("x")
        self.title_label.setText(self.tr("Filament Detector"))
        self.load_again_button.setText(self.tr("Load again."))
        self.next_button.setText(self.tr("Next"))
        self.update_message()

    def update_message(self):
        self.message_label.setText(
            f"{self.message_print}\n{self.message_unload}\n{self.message_clean}\n{self.message_load}")

    def start_load(self):
        self.message_load = self.tr("- Loading...")
        self.update_message()
        self.next_button.setText(self.tr("Resume Print."))
        self.load_again_button.show()
        self.load_again_button.setEnabled(False)
        self.next_button.setEnabled(False)
        timer_frame = 2
        self._printer.write_gcode_commands(f"G91\nG0\nG1 E{load_length} F{load_speed}\nG90\nM400")
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(int(load_time * timer_frame))
        self.working_progress = 0
        self.progress_bar.show()
        self.working_timer.start(int(1000 / timer_frame))

    def start_unload(self):
        timer_frame = 2
        self._printer.write_gcode_commands(f"G91\nG1 E{unload_purge_length} F{unload_purge_speed}\n"
                                           f"G1 E-{unload_length} F{unload_speed}\nG90\nM400")
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(int((unload_time + 5) * timer_frame))
        self.working_progress = 0
        self.progress_bar.show()
        self.working_timer.start(int(1000 / timer_frame))

    def goto_next_stage(self):
        if self.status == RunOutStatus.RUNOUT_NULL:
            self.status = RunOutStatus.RUNOUT_UNLOAD
            self.message_print = self.tr(
                "- A filament abnormality is detected and printing is paused.")
            self.message_unload = self.tr("- Unload the abnormal filament.")
            self.update_message()
            self.footer.hide()
            self.next_button.setEnabled(True)
            self.start_unload()
        elif self.status == RunOutStatus.RUNOUT_UNLOAD:
            self.status = RunOutStatus.RUNOUT_CLEAN
            self.message_clean = self.tr("- Please clean the nozzle or load the new filament.")
            self.update_message()
            self.progress_bar.hide()
            self.load_again_button.hide()
            self.footer.show()
        elif self.status == RunOutStatus.RUNOUT_CLEAN:
            self.status = RunOutStatus.RUNOUT_HEAT
            self.message_load = self.tr("- Heating...")
            self.update_message()
            if is_release:
                self.next_button.setEnabled(False)
            target = self._printer.printing_information["temperature"][self._printer.get_extruder()]
            self._printer.set_thermal(self._printer.get_extruder(), target if target >= 170 else 170)
        elif self.status == RunOutStatus.RUNOUT_HEAT:
            self.status = RunOutStatus.RUNOUT_LOAD
            self.start_load()
        elif self.status == RunOutStatus.RUNOUT_LOAD:
            self._printer.print_resume()
            self.status = RunOutStatus.RUNOUT_NULL
            self.load_again_button.hide()
            self.reject()

    def on_close_button_clicked(self):
        self.reject()

    def on_next_button_clicked(self):
        self.goto_next_stage()

    def on_working_timer_timeout(self):
        self.working_progress += 1
        self.progress_bar.setValue(self.working_progress)
        if self.working_progress > self.progress_bar.maximum():
            self.working_timer.stop()
            if self.status == RunOutStatus.RUNOUT_LOAD:
                self.message_load = self.tr(
                    "- Filament loading is completed, please choose to load again or resume printing.")
                self.update_message()
                self.load_again_button.setEnabled(True)
                self.next_button.setEnabled(True)
            else:
                self.goto_next_stage()

    def start(self):
        self.message_print = ""
        self.message_unload = ""
        self.message_clean = ""
        self.message_load = ""
        self.status = RunOutStatus.RUNOUT_NULL
        self.goto_next_stage()
        self.exec()

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        if self.status == RunOutStatus.RUNOUT_HEAT:
            if self._printer.get_temperature(self._printer.get_extruder()) + 3 >= self._printer.get_target(
                    self._printer.get_extruder()) > 170:
                self.message_load = self.tr("- Heating is complete.")
                self.update_message()
                if not self.next_button.isEnabled():
                    self.next_button.setEnabled(True)
