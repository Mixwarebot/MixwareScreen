import logging
import platform

from qtCore import *
from ui.base.baseLine import BaseHLine, BaseVLine
from ui.base.basePushButton import BasePushButton
from ui.base.handleBar import HandleBar
from ui.base.messageBar import MessageBar
from ui.levelPages.bedMeshGraph import BedMeshGraph


class DialIndicatorPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("dialIndicatorPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.message_frame = QFrame()
        self.message_frame.setObjectName("frameBox")
        self.message_frame.setFixedSize(360, 240)
        self.message_layout = QVBoxLayout(self.message_frame)
        self.message_layout.setContentsMargins(20, 20, 20, 20)
        self.message_layout.setSpacing(10)
        self.message_list = []
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Preheat extruder."),
            self.tr("Clean the nozzle."),
            self.tr("Place dial indicator."),
            self.tr("Measure compensation value(Left)."),
            self.tr("Measure compensation value(Right)."),
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
        self.preheat_thermal_frame.setFixedSize(360, 140)
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

        self.clean_handle = HandleBar()
        self.clean_handle.previous_button.hide()
        self.clean_handle.next_button.clicked.connect(self.on_clean_next_button_clicked)
        self.clean_body_layout = QVBoxLayout(self.clean_handle.body)
        self.clean_body_layout.setContentsMargins(20, 0, 20, 0)
        self.clean_body_layout.setSpacing(0)
        self.clean_body_layout.setAlignment(Qt.AlignCenter)
        self.clean_logo = QLabel()
        self.clean_logo.setFixedSize(320, 320)
        self.clean_logo.setScaledContents(True)
        self.clean_logo.setPixmap(QPixmap("resource/image/level_clean_nozzle.jpg"))
        self.clean_body_layout.addWidget(self.clean_logo)
        self.clean_text = QLabel()
        self.clean_text.setWordWrap(True)
        self.clean_text.setAlignment(Qt.AlignCenter)
        self.clean_body_layout.addWidget(self.clean_text)
        self.handle_stacked_widget.addWidget(self.clean_handle)

        self.place_handle = HandleBar()
        self.place_handle.previous_button.hide()
        self.place_handle.next_button.clicked.connect(self.on_place_next_button_clicked)
        self.place_body_layout = QVBoxLayout(self.place_handle.body)
        self.place_body_layout.setContentsMargins(20, 0, 20, 0)
        self.place_body_layout.setSpacing(0)
        self.place_body_layout.setAlignment(Qt.AlignCenter)
        self.place_logo = QLabel()
        self.place_logo.setFixedSize(320, 320)
        self.place_logo_movie = QMovie("resource/image/level_measure.gif")
        self.place_logo_movie.setScaledSize(self.remind_logo.size())
        self.place_logo.setMovie(self.place_logo_movie)
        self.place_body_layout.addWidget(self.place_logo)
        self.place_text = QLabel()
        self.place_text.setWordWrap(True)
        self.place_text.setAlignment(Qt.AlignCenter)
        self.place_body_layout.addWidget(self.place_text)
        self.handle_stacked_widget.addWidget(self.place_handle)

        self.measure_left_handle = HandleBar()
        self.measure_left_handle.previous_button.hide()
        self.measure_left_handle.next_button.clicked.connect(self.on_measure_left_next_button_clicked)
        self.measure_left_body_layout = QVBoxLayout(self.measure_left_handle.body)
        self.measure_left_body_layout.setContentsMargins(20, 0, 20, 0)
        self.measure_left_body_layout.setSpacing(0)
        self.measure_left_body_layout.setAlignment(Qt.AlignCenter)
        self.measure_left_logo = QLabel()
        self.measure_left_logo.setFixedSize(320, 320)
        self.measure_left_logo_movie = QMovie("resource/image/level_measure_left.gif")
        self.measure_left_logo_movie.setScaledSize(self.remind_logo.size())
        self.measure_left_logo.setMovie(self.measure_left_logo_movie)
        self.measure_left_body_layout.addWidget(self.measure_left_logo)
        self.measure_left_text = QLabel()
        self.measure_left_text.setWordWrap(True)
        self.measure_left_text.setAlignment(Qt.AlignCenter)
        self.measure_left_body_layout.addWidget(self.measure_left_text)
        self.handle_stacked_widget.addWidget(self.measure_left_handle)

        self.measure_right_handle = HandleBar()
        self.measure_right_handle.previous_button.hide()
        self.measure_right_handle.next_button.clicked.connect(self.on_measure_right_next_button_clicked)
        self.measure_right_body_layout = QVBoxLayout(self.measure_right_handle.body)
        self.measure_right_body_layout.setContentsMargins(20, 0, 20, 0)
        self.measure_right_body_layout.setSpacing(0)
        self.measure_right_body_layout.setAlignment(Qt.AlignCenter)
        self.measure_right_logo = QLabel()
        self.measure_right_logo.setFixedSize(320, 320)
        self.measure_right_logo_movie = QMovie("resource/image/level_measure_right.gif")
        self.measure_right_logo_movie.setScaledSize(self.remind_logo.size())
        self.measure_right_logo.setMovie(self.measure_right_logo_movie)
        self.measure_right_body_layout.addWidget(self.measure_right_logo)
        self.measure_right_text = QLabel()
        self.measure_right_text.setWordWrap(True)
        self.measure_right_text.setAlignment(Qt.AlignCenter)
        self.measure_right_body_layout.addWidget(self.measure_right_text)
        self.handle_stacked_widget.addWidget(self.measure_right_handle)

        self.finished_handle = HandleBar()
        self.finished_handle.previous_button.hide()
        self.finished_handle.next_button.clicked.connect(self.on_finished_next_button_clicked)
        self.finished_body_layout = QVBoxLayout(self.finished_handle.body)
        self.finished_body_layout.setContentsMargins(20, 0, 20, 0)
        self.finished_body_layout.setSpacing(0)
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
        self.place_logo_movie.stop()
        self.measure_left_logo_movie.stop()
        self.measure_right_logo_movie.stop()

    def reset_ui(self):
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Preheat extruder."),
            self.tr("Clean the nozzle."),
            self.tr("Place dial indicator."),
            self.tr("Measure compensation value(Left)."),
            self.tr("Measure compensation value(Right)."),
            self.tr("Finish.")
        ]
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
            if count < 3:
                self.message_list[count].show()
            else:
                self.message_list[count].hide()
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def re_translate_ui(self):
        self.remind_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.preheat_thermal_left_button.setText("-")
        self.preheat_thermal_right_button.setText("-")
        self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 170°C)"))
        self.preheat_pla.setText("PLA")
        self.preheat_abs.setText("ABS")
        self.preheat_pet.setText("PET")
        self.preheat_pa.setText("PA")
        self.clean_text.setText(self.tr("Please use a metal brush to clean the nozzle residue."))
        self.place_text.setText(self.tr("Place the dial indicator at the specified location."))
        self.measure_left_text.setText(self.tr("Click <Next> to start measure compensation value(Left)."))
        self.measure_right_text.setText(self.tr("Click <Next> to start measure compensation value(Right)."))
        self.finished_text.setText(self.tr("Measure completed."))

    @pyqtSlot()
    def on_update_printer_information(self):
        self.preheat_thermal_left_button.setText(self._printer.get_thermal('left'))
        self.preheat_thermal_right_button.setText(self._printer.get_thermal('right'))

        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 170 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170:
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))

    def goto_previous_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index > 0:
            self.message_list[index].setEnabled(False)
            self.message_list[index - 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index - 1)
            if 1 < index < self.handle_stacked_widget.count():
                self.message_list[index + 1].hide()
                self.message_list[index - 2].show()

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)
            if 0 < index < (self.handle_stacked_widget.count() - 2):
                self.message_list[index - 1].hide()
                self.message_list[index + 2].show()

    def on_remind_next_button_clicked(self):
        if platform.system().lower() == 'linux':
            self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        # preheat -> 170
        self._printer.set_thermal('left', 170)
        self._printer.set_thermal('right', 170)
        self._printer.write_gcode_commands("M155 S1\nG28\nT0\nG1 X0 Y20 Z50 F8400\nM155 S0")

    def reset_preheat_handle_ui(self):
        if platform.system().lower() == 'linux':
            if self.preheat_handle.next_button.isEnabled():
                self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 170°C)"))
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

    def on_preheat_pla_clicked(self):
        self.preheat_filament(210)

    def on_preheat_abs_clicked(self):
        self.preheat_filament(240)

    def on_preheat_pet_clicked(self):
        self.preheat_filament(270)

    def on_preheat_pa_clicked(self):
        self.preheat_filament(300)

    def on_preheat_next_button_clicked(self):
        self.goto_next_step_stacked_widget()

    def on_clean_next_button_clicked(self):
        # if platform.system().lower() == 'linux':
        self._printer.set_thermal('left', 0)
        self._printer.set_thermal('right', 0)
        self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y160 Z150 F8400")

        self.goto_next_step_stacked_widget()
        self.place_logo_movie.start()

    def on_place_next_button_clicked(self):
        self.goto_next_step_stacked_widget()
        self.place_logo_movie.stop()
        self.measure_left_logo_movie.start()

    def on_measure_left_next_button_clicked(self):
        self._printer.write_gcode_commands(
            "G1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F360\nM400")
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(self.tr("Please enter the value from the dial indicator."),
                                         "dial_indicator_left")
        self._printer.write_gcode_commands(
            "G1 Z150 F960\nM400\nG28\nG1 Y160 Z150 F8400\nM400\nT1\nG1 X190 Z150 F8400\nM400")
        self.goto_next_step_stacked_widget()
        self.measure_left_logo_movie.stop()
        self.measure_right_logo_movie.start()

    def on_measure_right_next_button_clicked(self):
        self._printer.write_gcode_commands(
            "G1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F360\nM400")
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(self.tr("Please enter the value from the dial indicator."),
                                         "dial_indicator_right")
        self._printer.write_gcode_commands("G1 Z150 F960\nM400\nG28X")
        self.goto_next_step_stacked_widget()
        self.measure_right_logo_movie.stop()

    def on_finished_next_button_clicked(self):
        self._printer.save_dial_indicator_value()
        self._parent.footer.setEnabled(True)
        self.reset_ui()
        self._parent.gotoPreviousPage()
        self.finished_handle.next_button.setText(self.tr("Done."))
