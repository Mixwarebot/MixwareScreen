import logging
import platform

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
            self.tr("Clean platform debris."),
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
        # self.work_logo = QLabel()
        # self.work_logo.setFixedSize(320, 320)
        # self.work_logo.setScaledContents(True)
        # self.work_logo.setPixmap(QPixmap("resource/image/level_clean_nozzle.jpg"))
        # self.work_body_layout.addWidget(self.work_logo)
        self.work_text = QLabel()
        self.work_text.setWordWrap(True)
        self.work_text.setAlignment(Qt.AlignCenter)
        self.work_body_layout.addWidget(self.work_text)
        self.handle_stacked_widget.addWidget(self.work_handle)

        self.finished_handle = HandleBar()
        self.finished_handle.previous_button.hide()
        self.finished_handle.next_button.clicked.connect(self.on_finished_next_button_clicked)
        self.finished_body_layout = QVBoxLayout(self.finished_handle.body)
        self.finished_body_layout.setContentsMargins(0, 0, 0, 0)
        self.finished_body_layout.setSpacing(0)

        self.finished_offset_frame = QFrame()
        self.finished_offset_frame.setFixedSize(360, 148)
        self.finished_offset_frame_layout = QGridLayout(self.finished_offset_frame)
        self.finished_offset_frame_layout.setContentsMargins(20, 10, 20, 10)
        self.finished_offset_frame_layout.setSpacing(0)
        self.finished_offset_x = QLabel()
        self.finished_offset_x.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.finished_offset_x.setText("X offset: ")
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x, 0, 0, 1, 1)
        self.finished_offset_x_button = QPushButton()
        self.finished_offset_x_button.setFixedHeight(64)
        self.finished_offset_x_button.clicked.connect(self.on_finished_offset_x_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_button, 0, 1, 2, 1)
        self.finished_offset_x_tips = QLabel()
        self.finished_offset_x_tips.setObjectName('tips')
        self.finished_offset_x_tips.setFixedHeight(24)
        self.finished_offset_x_tips.setAlignment(Qt.AlignCenter)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_x_tips, 1, 0, 1, 1)
        self.finished_offset_frame_layout.addWidget(BaseHLine(), 2, 0, 1, 2)
        self.finished_offset_y = QLabel()
        self.finished_offset_y.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.finished_offset_y.setText("Y offset: ")
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y, 3, 0, 1, 1)
        self.finished_offset_y_button = QPushButton()
        self.finished_offset_y_button.setFixedHeight(64)
        self.finished_offset_y_button.clicked.connect(self.on_finished_offset_y_button_clicked)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_button, 3, 1, 2, 1)
        self.finished_offset_y_tips = QLabel()
        self.finished_offset_y_tips.setObjectName('tips')
        self.finished_offset_y_tips.setFixedHeight(24)
        self.finished_offset_y_tips.setAlignment(Qt.AlignCenter)
        self.finished_offset_frame_layout.addWidget(self.finished_offset_y_tips, 4, 0, 1, 1)
        self.finished_body_layout.addWidget(self.finished_offset_frame)
        self.finished_body_layout.addWidget(BaseHLine())

        self.finished_text = QLabel()
        self.finished_text.setWordWrap(True)
        self.finished_text.setAlignment(Qt.AlignCenter)
        self.finished_body_layout.addWidget(self.finished_text)
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
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def re_translate_ui(self):
        self.remind_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.preheat_thermal_left_button.setText("-")
        self.preheat_thermal_right_button.setText("-")
        self.preheat_thermal_bed_button.setText("-")
        self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 210°C)"))
        self.preheat_pla.setText("PLA")
        self.preheat_abs.setText("ABS")
        self.preheat_pet.setText("PET")
        self.preheat_pa.setText("PA")
        self.work_thermal_left_button.setText("-")
        self.work_thermal_right_button.setText("-")
        self.work_thermal_bed_button.setText("-")
        self.work_text.setText(self.tr("Please wait."))
        self.finished_handle.next_button.setText(self.tr("Done"))
        self.finished_offset_x_button.setText('0')
        self.finished_offset_y_button.setText('0')
        self.finished_offset_x_tips.setText("<: -; >: +")
        self.finished_offset_y_tips.setText("∧: -; ∨: +")
        self.finished_text.setText(self.tr("Measure completed.\nPlease enter offset."))

    @pyqtSlot()
    def on_update_printer_information(self):
        self.preheat_thermal_left_button.setText(self._printer.get_thermal('left'))
        self.preheat_thermal_right_button.setText(self._printer.get_thermal('right'))
        self.preheat_thermal_bed_button.setText(self._printer.get_thermal('bed'))
        self.work_thermal_left_button.setText(self._printer.get_thermal('left'))
        self.work_thermal_right_button.setText(self._printer.get_thermal('right'))
        self.work_thermal_bed_button.setText(self._printer.get_thermal('bed'))

        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 170 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170 \
                    and self._printer.get_temperature('bed') + 3 >= self._printer.get_target('bed'):
                logging.debug(f"Heat completed.")
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))
        elif self.handle_stacked_widget.currentWidget() == self.work_handle:
            if not self._printer.is_print_verify():
                self.goto_next_step_stacked_widget()

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)

    def on_remind_next_button_clicked(self):
        logging.debug(f"Start preheat")
        if platform.system().lower() == 'linux':
            self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        # preheat -> 210
        self._printer.set_thermal('left', 210)
        self._printer.set_thermal('right', 210)
        self._printer.set_thermal('bed', 60)
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

    def on_preheat_abs_clicked(self):
        self.preheat_filament(240)

    def on_preheat_pet_clicked(self):
        self.preheat_filament(270)

    def on_preheat_pa_clicked(self):
        self.preheat_filament(300)

    def on_preheat_next_button_clicked(self):
        if platform.system().lower() == 'linux':
            self.work_handle.next_button.setEnabled(False)
        self._printer.print_verify()
        self.goto_next_step_stacked_widget()

    def on_clean_next_button_clicked(self):
        if platform.system().lower() == 'linux':
            self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y20 Z150 F8400")

        self.goto_next_step_stacked_widget()

    def on_finished_offset_x_button_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"Please enter x offset", "")
        self.finished_offset_x_button.setText(self._parent.numberPad.number)

    def on_finished_offset_y_button_clicked(self):
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(f"Please enter y offset", "")
        self.finished_offset_y_button.setText(self._parent.numberPad.number)

    def on_finished_next_button_clicked(self):
        self._printer.save_right_offset('X', self._printer.information['probe']['offset']['right']['X'] + float(
            self.finished_offset_x_button.text()))
        self._printer.save_right_offset('Y', self._printer.information['probe']['offset']['right']['Y'] + float(
            self.finished_offset_y_button.text()))
        self.reset_ui()
        self._parent.gotoPreviousPage()
