import logging
import platform
import re

from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.base.baseLine import BaseHLine, BaseVLine
from ui.base.basePushButton import BasePushButton
from ui.base.handleBar import HandleBar
from ui.base.messageBar import MessageBar


class PrintVerifyPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("printVerifyPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.message_frame = QFrame()
        self.message_frame.setObjectName("frameBox")
        self.message_frame.setFixedSize(360, 310)
        self.message_layout = QVBoxLayout(self.message_frame)
        self.message_layout.setContentsMargins(20, 20, 20, 20)
        self.message_layout.setSpacing(10)
        self.message_list = []
        self.message_text_list = [
            self.tr("Clear debris from the platform."),
            self.tr("Preheat extruder."),
            self.tr("Working."),
            self.tr("Finish.")
        ]
        for i in range(len(self.message_text_list)):
            self.message_list.append(MessageBar(i + 1, self.message_text_list[i]))
            self.message_layout.addWidget(self.message_list[i])
        self.layout.addWidget(self.message_frame)

        self.handle_frame = QFrame()
        self.handle_frame.setFixedWidth(360)
        self.handle_frame.setObjectName("frameBox")
        self.handle_frame_layout = QVBoxLayout(self.handle_frame)
        self.handle_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.handle_frame_layout.setSpacing(10)
        self.handle_stacked_widget = QStackedWidget()
        self.handle_stacked_widget.setContentsMargins(0, 0, 0, 0)

        self.remind_handle = HandleBar()
        self.remind_handle.previous_button.hide()
        self.remind_handle.next_button.clicked.connect(self.on_remind_next_button_clicked)
        self.remind_body_layout = QVBoxLayout(self.remind_handle.body)
        self.remind_body_layout.setContentsMargins(20, 0, 20, 0)
        self.remind_body_layout.setSpacing(0)
        self.remind_body_layout.setAlignment(Qt.AlignCenter)
        self.remind_logo = QLabel()
        self.remind_logo.setFixedSize(320, 320)
        self.remind_logo.setScaledContents(True)
        self.remind_logo.setPixmap(QPixmap("resource/image/level_clean_bed.png"))
        self.remind_body_layout.addWidget(self.remind_logo)
        self.remind_text = QLabel()
        self.remind_text.setWordWrap(True)
        self.remind_text.setAlignment(Qt.AlignCenter)
        self.remind_body_layout.addWidget(self.remind_text)
        self.handle_stacked_widget.addWidget(self.remind_handle)

        self.preheat_handle = HandleBar()
        self.preheat_handle.previous_button.hide()
        self.preheat_handle.next_button.clicked.connect(self.on_preheat_next_button_clicked)
        self.preheat_body_layout = QVBoxLayout(self.preheat_handle.body)
        self.preheat_body_layout.setContentsMargins(0, 0, 0, 0)
        self.preheat_body_layout.setSpacing(0)

        self.preheat_thermal_frame = QFrame()
        self.preheat_thermal_frame.setFixedSize(360, 210)
        self.preheat_thermal_frame_layout = QGridLayout(self.preheat_thermal_frame)
        self.preheat_thermal_frame_layout.setContentsMargins(10, 10, 10, 0)
        self.preheat_thermal_frame_layout.setSpacing(0)
        self.preheat_thermal_left = QLabel()
        self.preheat_thermal_left.setObjectName("leftLogo")
        self.preheat_thermal_frame_layout.addWidget(self.preheat_thermal_left, 0, 0, 1, 1)
        self.preheat_thermal_left_button = QPushButton()
        self.preheat_thermal_left_button.setFixedHeight(64)
        self.preheat_thermal_left_button.clicked.connect(self.on_preheat_thermal_left_button_clicked)
        self.preheat_thermal_frame_layout.addWidget(self.preheat_thermal_left_button, 0, 1, 1, 1)
        self.preheat_thermal_frame_layout.addWidget(BaseHLine(), 1, 0, 1, 2)
        self.preheat_thermal_right = QLabel()
        self.preheat_thermal_right.setObjectName("rightLogo")
        self.preheat_thermal_frame_layout.addWidget(self.preheat_thermal_right, 2, 0, 1, 1)
        self.preheat_thermal_right_button = QPushButton()
        self.preheat_thermal_right_button.setFixedHeight(64)
        self.preheat_thermal_right_button.clicked.connect(self.on_preheat_thermal_right_button_clicked)
        self.preheat_thermal_frame_layout.addWidget(self.preheat_thermal_right_button, 2, 1, 1, 1)
        self.preheat_thermal_frame_layout.addWidget(BaseHLine(), 3, 0, 1, 2)
        self.preheat_thermal_bed = QLabel()
        self.preheat_thermal_bed.setObjectName("bedLogo")
        self.preheat_thermal_frame_layout.addWidget(self.preheat_thermal_bed, 4, 0, 1, 1)
        self.preheat_thermal_bed_button = QPushButton()
        self.preheat_thermal_bed_button.setFixedHeight(64)
        self.preheat_thermal_bed_button.clicked.connect(self.on_preheat_thermal_bed_button_clicked)
        self.preheat_thermal_frame_layout.addWidget(self.preheat_thermal_bed_button, 4, 1, 1, 1)
        self.preheat_body_layout.addWidget(self.preheat_thermal_frame)
        self.preheat_body_layout.addWidget(BaseHLine())
        self.preheat_filament_layout = QHBoxLayout()
        self.preheat_pla = BasePushButton()
        self.preheat_pla.setFixedHeight(64)
        self.preheat_pla.clicked.connect(self.on_preheat_pla_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_pla)
        self.preheat_filament_layout.addWidget(BaseVLine())
        self.preheat_abs = BasePushButton()
        self.preheat_abs.setFixedHeight(64)
        self.preheat_abs.clicked.connect(self.on_preheat_abs_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_abs)
        self.preheat_filament_layout.addWidget(BaseVLine())
        self.preheat_pet = BasePushButton()
        self.preheat_pet.setFixedHeight(64)
        self.preheat_pet.clicked.connect(self.on_preheat_pet_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_pet)
        self.preheat_filament_layout.addWidget(BaseVLine())
        self.preheat_pa = BasePushButton()
        self.preheat_pa.setFixedHeight(64)
        self.preheat_pa.clicked.connect(self.on_preheat_pa_clicked)
        self.preheat_filament_layout.addWidget(self.preheat_pa)
        self.preheat_body_layout.addLayout(self.preheat_filament_layout)
        self.preheat_body_layout.addWidget(BaseHLine())
        self.preheat_text = QLabel()
        self.preheat_text.setWordWrap(True)
        self.preheat_text.setAlignment(Qt.AlignCenter)
        self.preheat_body_layout.addWidget(self.preheat_text)
        self.handle_stacked_widget.addWidget(self.preheat_handle)

        self.work_handle = HandleBar()
        self.work_handle.previous_button.hide()
        self.work_handle.next_button.clicked.connect(self.on_clean_next_button_clicked)
        self.work_body_layout = QVBoxLayout(self.work_handle.body)
        self.work_body_layout.setContentsMargins(0, 0, 0, 0)
        self.work_body_layout.setSpacing(0)
        # self.work_body_layout.setAlignment(Qt.AlignCenter)
        self.work_thermal_frame = QFrame()
        self.work_thermal_frame.setFixedSize(360, 210)
        self.work_thermal_frame_layout = QGridLayout(self.work_thermal_frame)
        self.work_thermal_frame_layout.setContentsMargins(10, 10, 10, 0)
        self.work_thermal_frame_layout.setSpacing(0)
        self.work_thermal_left = QLabel()
        self.work_thermal_left.setObjectName("leftLogo")
        self.work_thermal_frame_layout.addWidget(self.work_thermal_left, 0, 0, 1, 1)
        self.work_thermal_left_button = QPushButton()
        self.work_thermal_left_button.setFixedHeight(64)
        self.work_thermal_left_button.clicked.connect(self.on_preheat_thermal_left_button_clicked)
        self.work_thermal_frame_layout.addWidget(self.work_thermal_left_button, 0, 1, 1, 1)
        self.work_thermal_frame_layout.addWidget(BaseHLine(), 1, 0, 1, 2)
        self.work_thermal_right = QLabel()
        self.work_thermal_right.setObjectName("rightLogo")
        self.work_thermal_frame_layout.addWidget(self.work_thermal_right, 2, 0, 1, 1)
        self.work_thermal_right_button = QPushButton()
        self.work_thermal_right_button.setFixedHeight(64)
        self.work_thermal_right_button.clicked.connect(self.on_preheat_thermal_right_button_clicked)
        self.work_thermal_frame_layout.addWidget(self.work_thermal_right_button, 2, 1, 1, 1)
        self.work_thermal_frame_layout.addWidget(BaseHLine(), 3, 0, 1, 2)
        self.work_thermal_bed = QLabel()
        self.work_thermal_bed.setObjectName("bedLogo")
        self.work_thermal_frame_layout.addWidget(self.work_thermal_bed, 4, 0, 1, 1)
        self.work_thermal_bed_button = QPushButton()
        self.work_thermal_bed_button.setFixedHeight(64)
        self.work_thermal_bed_button.clicked.connect(self.on_preheat_thermal_bed_button_clicked)
        self.work_thermal_frame_layout.addWidget(self.work_thermal_bed_button, 4, 1, 1, 1)
        self.work_body_layout.addWidget(self.work_thermal_frame)
        self.work_body_layout.addWidget(BaseHLine())
        self.verity_model_logo = QLabel()
        self.verity_model_logo.setFixedSize(360, 540)
        self.verity_model_logo.setAlignment(Qt.AlignCenter)
        self.verity_model_logo.setPixmap(QPixmap("resource/image/xy_verity").scaledToWidth(320))
        self.work_body_layout.addWidget(self.verity_model_logo)
        self.work_text = QLabel()
        self.work_text.setWordWrap(True)
        self.work_text.setAlignment(Qt.AlignCenter)
        self.work_body_layout.addWidget(self.work_text)
        self.work_progress_bar = QProgressBar()
        self.work_progress_bar.setTextVisible(False)
        self.work_progress_bar.setFixedHeight(18)
        self.work_body_layout.addWidget(self.work_progress_bar)
        self.handle_stacked_widget.addWidget(self.work_handle)

        self.finished_handle = HandleBar()
        self.finished_handle.previous_button.hide()
        self.finished_handle.next_button.clicked.connect(self.on_finished_next_button_clicked)
        self.finished_body_layout = QVBoxLayout(self.finished_handle.body)
        self.finished_body_layout.setContentsMargins(0, 20, 0, 0)
        self.finished_body_layout.setSpacing(0)
        self.verity_logo = QLabel()
        self.verity_logo.setFixedSize(320, 320)
        self.verity_logo.setStyleSheet("padding-left: 20px; padding-top: 20px;")
        self.verity_movie = QMovie("resource/image/verity.gif")
        self.verity_movie.setScaledSize(self.verity_logo.size())
        self.verity_logo.setMovie(self.verity_movie)
        self.finished_body_layout.addWidget(self.verity_logo)
        self.finished_text = QLabel()
        self.finished_text.setWordWrap(True)
        self.finished_text.setAlignment(Qt.AlignCenter)
        self.finished_body_layout.addWidget(self.finished_text)

        self.finished_offset_frame = QFrame()
        self.finished_offset_frame.setFixedSize(360, 148)
        self.finished_offset_frame_layout = QGridLayout(self.finished_offset_frame)
        self.finished_offset_frame_layout.setContentsMargins(20, 10, 20, 10)
        self.finished_offset_frame_layout.setSpacing(0)
        self.finished_distance_frame = QFrame()
        self.finished_distance_frame.setFixedHeight(128)
        self.finished_distance_frame_layout = QVBoxLayout(self.finished_distance_frame)
        self.finished_distance_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.finished_distance_frame_layout.setSpacing(0)
        self.finished_distance_title = QLabel()
        self.finished_distance_title.setObjectName("frame_title")
        self.finished_distance_title.setFixedHeight(40)
        self.finished_distance_frame_layout.addWidget(self.finished_distance_title)
        self.finished_distance_button_frame = QFrame()
        self.finished_distance_button_frame.setObjectName("frameBox")
        self.finished_distance_button_frame.setFixedHeight(88)
        self.finished_distance_button_frame_layout = QHBoxLayout(self.finished_distance_button_frame)
        self.finished_distance_button_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.finished_distance_button_frame_layout.setSpacing(0)
        self._button_group = QButtonGroup()
        self._button_group.buttonClicked.connect(self.on_offset_distance_button_clicked)
        self._distance_list = ["0.01", "0.05", "0.1", "0.5", "1"]
        self._distance_default = "0.1"
        self._distance_current_id = 0
        for d in range(len(self._distance_list)):
            button = BasePushButton()
            button.setText(self._distance_list[d])
            button.setObjectName("dataButton")
            self._button_group.addButton(button, d)
            if self._distance_list[d] == self._distance_default:
                self.on_offset_distance_button_clicked(
                    self._button_group.button(d))
            self.finished_distance_button_frame_layout.addWidget(button)
        self.finished_distance_frame_layout.addWidget(self.finished_distance_button_frame)
        self.finished_body_layout.addWidget(self.finished_distance_frame)
        self.finished_offset_frame = QFrame()
        self.finished_offset_frame.setFixedSize(360, 210)
        self.finished_offset_frame_layout = QGridLayout(self.finished_offset_frame)
        self.finished_offset_frame_layout.setContentsMargins(10, 0, 10, 0)
        self.finished_offset_frame_layout.setSpacing(0)
        self.finished_offset_x_label = QLabel()
        self.finished_offset_x_label.setAlignment(Qt.AlignCenter)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_label, 0, 0, 1, 2)
        self.finished_offset_x_dec_button = QPushButton()
        self.finished_offset_x_dec_button.setObjectName("leftLogo")
        self.finished_offset_x_dec_button.setFixedHeight(48)
        self.finished_offset_x_dec_button.clicked.connect(self.on_finished_offset_x_dec_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_dec_button, 0, 2, 1, 1)
        self.finished_offset_x_add_button = QPushButton()
        self.finished_offset_x_add_button.setObjectName("rightLogo")
        self.finished_offset_x_add_button.setFixedHeight(48)
        self.finished_offset_x_add_button.clicked.connect(self.on_finished_offset_x_add_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_add_button, 0, 3, 1, 1)
        self.finished_offset_frame_layout.addWidget(BaseHLine(), 1, 0, 1, 4)
        self.finished_offset_y_label = QLabel()
        self.finished_offset_y_label.setAlignment(Qt.AlignCenter)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_label, 2, 0, 1, 2)
        self.finished_offset_y_dec_button = QPushButton()
        self.finished_offset_y_dec_button.setObjectName("downLogo")
        self.finished_offset_y_dec_button.setFixedHeight(48)
        self.finished_offset_y_dec_button.clicked.connect(self.on_finished_offset_y_dec_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_dec_button, 2, 2, 1, 1)
        self.finished_offset_y_add_button = QPushButton()
        self.finished_offset_y_add_button.setObjectName("upLogo")
        self.finished_offset_y_add_button.setFixedHeight(48)
        self.finished_offset_y_add_button.clicked.connect(self.on_finished_offset_y_add_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_add_button, 2, 3, 1, 1)
        self.finished_body_layout.addWidget(self.finished_offset_frame)
        self.finished_body_layout.addWidget(BaseHLine())

        self.handle_stacked_widget.addWidget(self.finished_handle)
        self.handle_frame_layout.addWidget(self.handle_stacked_widget)
        self.layout.addWidget(self.handle_frame)

        self.reset_ui()
        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def hideEvent(self, a0: QHideEvent) -> None:
        pass

    def reset_ui(self):
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Preheat extruder."),
            self.tr("Working."),
            self.tr("Finish.")
        ]
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def re_translate_ui(self):
        self.remind_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 210°C)"))
        self.work_text.setText(self.tr("Verification model printing, please wait."))
        self.finished_handle.next_button.setText(self.tr("Done"))
        self.finished_distance_title.setText(self.tr("Move Distance (mm)"))
        self.finished_text.setText(self.tr(
            "Observe the XY test model, find aligned lines, with each grid measuring 0.1mm, and adjust the offset values of the left and right nozzles."))

        self.preheat_thermal_left_button.setText("-")
        self.preheat_thermal_right_button.setText("-")
        self.preheat_thermal_bed_button.setText("-")
        self.preheat_pla.setText("PLA")
        self.preheat_abs.setText("ABS")
        self.preheat_pet.setText("PET")
        self.preheat_pa.setText("PA")
        self.work_thermal_left_button.setText("-")
        self.work_thermal_right_button.setText("-")
        self.work_thermal_bed_button.setText("-")
        self.finished_offset_x_label.setText("X: 0.0")
        self.finished_offset_y_label.setText("Y: 0.0")

    @pyqtSlot()
    def on_update_printer_information(self):
        self.preheat_thermal_left_button.setText(self._printer.get_thermal('left'))
        self.preheat_thermal_right_button.setText(self._printer.get_thermal('right'))
        self.preheat_thermal_bed_button.setText(self._printer.get_thermal('bed'))
        self.work_thermal_left_button.setText(self._printer.get_thermal('left'))
        self.work_thermal_right_button.setText(self._printer.get_thermal('right'))
        self.work_thermal_bed_button.setText(self._printer.get_thermal('bed'))

        if self._printer.is_print_verify():
            self.work_progress_bar.setValue(int(self._printer.print_progress() * 100))

        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 170 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170 \
                    and self._printer.get_temperature('bed') + 3 >= self._printer.get_target('bed'):
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))
        elif self.handle_stacked_widget.currentWidget() == self.work_handle:
            if not self._printer.is_print_verify():
                self.goto_next_step_stacked_widget()
                self.verity_movie.start()

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, state):
        if state == MixwareScreenPrinterStatus.PRINTER_VERITY:
            self.work_thermal_frame.hide()
            self.work_text.setText(
                "Printing is completed.")
            self.work_handle.next_button.setEnabled(True)

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)

    @pyqtSlot(QAbstractButton)
    def on_offset_distance_button_clicked(self, button):
        if button.text() in self._distance_list:
            if self._button_group.id(button) != self._distance_current_id:
                self._button_group.button(self._distance_current_id).setStyleSheet(uncheckedStyleSheet)
                self._button_group.button(self._button_group.id(button)).setStyleSheet(checkedStyleSheet)
                self._distance_current_id = self._button_group.id(button)

    def on_remind_next_button_clicked(self):
        if platform.system().lower() == 'linux':
            self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        # preheat -> 210
        self._printer.set_thermal('left', 210)
        self._printer.set_thermal('right', 210)
        self._printer.set_thermal('bed', 60)
        update_style(self.preheat_pla, "checked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")
        self._printer.write_gcode_commands("M155 S2\nG28\nT0\nG1 X0 Y20 Z50 F8400\nM155 S0")

    def reset_preheat_handle_ui(self):
        if platform.system().lower() == 'linux':
            if self.preheat_handle.next_button.isEnabled():
                self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 210°C)"))
                self.preheat_handle.next_button.setEnabled(False)

    def preheat_filament(self, temperature):
        self._printer.set_thermal('left', temperature)
        self._printer.set_thermal('right', temperature)
        self.reset_preheat_handle_ui()

    def on_preheat_thermal_left_button_clicked(self):
        self._parent.open_thermal_left_numberPad()
        self.reset_preheat_handle_ui()

    def on_preheat_thermal_right_button_clicked(self):
        self._parent.open_thermal_right_numberPad()
        self.reset_preheat_handle_ui()

    def on_preheat_thermal_bed_button_clicked(self):
        self._parent.open_thermal_bed_numberPad()
        self.reset_preheat_handle_ui()

    def on_preheat_pla_clicked(self):
        self.preheat_filament(210)
        update_style(self.preheat_pla, "checked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")

    def on_preheat_abs_clicked(self):
        self.preheat_filament(240)
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "checked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")

    def on_preheat_pet_clicked(self):
        self.preheat_filament(270)
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "checked")

    def on_preheat_pa_clicked(self):
        self.preheat_filament(300)
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "checked")
        update_style(self.preheat_pet, "unchecked")

    def on_preheat_next_button_clicked(self):
        if platform.system().lower() == 'linux':
            self.work_handle.next_button.setEnabled(False)
        self._printer.print_verify()
        self.goto_next_step_stacked_widget()

    def on_clean_next_button_clicked(self):
        if platform.system().lower() == 'linux':
            self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y20 Z150 F8400")

        self.goto_next_step_stacked_widget()
        self.finished_handle.next_button.setText(self.tr("Done."))

    def on_finished_offset_x_dec_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.finished_offset_x_label.text())
        offset = float(text[0])
        offset += float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        self.finished_offset_x_label.setText(f"X: {offset}")

    def on_finished_offset_x_add_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.finished_offset_x_label.text())
        offset = float(text[0])
        offset -= float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        self.finished_offset_x_label.setText(f"X: {offset}")

    def on_finished_offset_y_dec_button_clicked(self):
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.finished_offset_y_label.text())
        offset = float(text[0])
        offset -= float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        self.finished_offset_y_label.setText(f"Y: {offset}")

    def on_finished_offset_y_add_button_clicked(self):
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.finished_offset_y_label.text())
        offset = float(text[0])
        offset += float(self._distance_list[self._distance_current_id - len(self._distance_list)])
        self.finished_offset_y_label.setText(f"Y: {offset}")

    def on_finished_next_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.finished_offset_x_label.text())
        hotend_offset_x = float(text[0])
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.finished_offset_y_label.text())
        hotend_offset_y = float(text[0])
        self._printer.set_hotend_offset('X', self._printer.information['probe']['offset']['right']['X'] + float(
            hotend_offset_x))
        self._printer.set_hotend_offset('Y', self._printer.information['probe']['offset']['right']['Y'] + float(
            hotend_offset_y))
        self.reset_ui()
        self.verity_movie.stop()
        self._parent.gotoPreviousPage()
