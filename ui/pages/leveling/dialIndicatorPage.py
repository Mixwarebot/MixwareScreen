import platform

from qtCore import *
from ui.components.base.baseLine import BaseHLine, BaseVLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.baseTitleFrame import BaseTitleFrame
from ui.components.handleBar import HandleBar
from ui.components.messageBar import MessageBar
from ui.components.movieLabel import MovieLabel
from ui.components.preHeatWidget import PreHeatWidget


class DialIndicatorPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._parent = parent
        self.message_text_list = None

        self.setObjectName("dialIndicatorPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.reset_message_title()
        self.message_frame = BaseTitleFrame()
        self.message_list = self.message_frame.set_message(self.message_text_list)
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

        self.remind_logo = MovieLabel("resource/image/clean_bed.gif", 320, 320)
        self.remind_logo.setFixedSize(320, 320)
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
        self.preheat_body_layout.setContentsMargins(20, 0, 20, 0)
        self.preheat_body_layout.setSpacing(0)

        self.preheat_filament = PreHeatWidget(self._printer, self._parent, False)
        self.preheat_filament.preheat_changed.connect(self.reset_preheat_handle_ui)
        self.preheat_body_layout.addWidget(self.preheat_filament)
        self.preheat_text = QLabel()
        self.preheat_text.setWordWrap(True)
        self.preheat_text.setAlignment(Qt.AlignCenter)
        self.preheat_body_layout.addWidget(self.preheat_text)
        self.handle_stacked_widget.addWidget(self.preheat_handle)

        self.clean_handle = HandleBar()
        self.clean_handle.previous_button.hide()
        self.clean_timer = QTimer()
        self.clean_timer.timeout.connect(self.on_clean_timer_timeout)
        self.clean_handle.next_button.clicked.connect(self.on_clean_next_button_clicked)

        self.clean_body_layout = QVBoxLayout(self.clean_handle.body)
        self.clean_body_layout.setContentsMargins(20, 0, 20, 0)
        self.clean_body_layout.setSpacing(0)
        self.clean_body_layout.setAlignment(Qt.AlignCenter)

        self.clean_logo = MovieLabel("resource/image/clean_nozzle.gif", 320, 220)
        self.clean_logo.setFixedSize(320, 220)
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

        self.place_logo = MovieLabel("resource/image/level_measure.gif", 320, 320)
        self.place_logo.setFixedSize(320, 320)
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

        self.measure_left_logo = MovieLabel("resource/image/level_measure_left.gif", 320, 320)
        self.measure_left_logo.setFixedSize(320, 320)
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

        self.measure_right_logo = MovieLabel("resource/image/level_measure_right.gif", 320, 320)
        self.measure_right_logo.setFixedSize(320, 320)
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

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def reset_ui(self):
        self.reset_message_title()
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
        self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 170°C)"))
        self.clean_text.setText(self.tr("Please use a metal brush to clean the nozzle residue."))
        self.place_text.setText(self.tr("Place the dial indicator at the specified location."))
        self.measure_left_text.setText(self.tr("Click <Next> to start measure compensation value(Left)."))
        self.measure_right_text.setText(self.tr("Click <Next> to start measure compensation value(Right)."))
        self.finished_text.setText(self.tr("Measure completed."))

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return

        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 0 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 0:
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
        if is_release:
            self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        # preheat -> 170, 170
        self._printer.write_gcode_command("T0\nM155 S1\nM104 S170 T0\nM104 S170 T1")
        self._printer.auto_home()
        self._printer.move_to_xy(0, 20, wait=True)
        self._printer.move_to_z(150, wait=True)
        self._printer.write_gcode_command("M155 S0")

    def reset_preheat_handle_ui(self):
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

    def on_preheat_next_button_clicked(self):
        self._printer.write_gcode_command('M400\nM104 S0 T0\nM104 S0 T1\nT0')
        self._printer.move_to_x(190, wait=True)
        self.clean_handle.next_button.setEnabled(False)
        self.clean_timer.start(1900)
        self.goto_next_step_stacked_widget()

    def on_clean_timer_timeout(self):
        self.clean_timer.stop()
        self.clean_handle.next_button.setEnabled(True)

    def on_clean_next_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_command('T1')
            self._printer.move_to_x(190, wait=True)
            self.clean_handle.next_button.setEnabled(False)
            self.clean_timer.start(4000)
        else:
            self._printer.write_gcode_command('T0')
            self._printer.auto_home()
            self._printer.move_to_xy(190, 160, wait=True)
            self._printer.move_to_z(150, wait=True)
            self.goto_next_step_stacked_widget()

    def on_place_next_button_clicked(self):
        self.goto_next_step_stacked_widget()

    def on_measure_left_next_button_clicked(self):
        self._printer.write_gcode_commands(
            "G1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F320\nM400")
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(self.tr("Please enter the absolute value from the dial indicator."),
                                         "dial_indicator_left")
        self._printer.write_gcode_commands(
            "G1 Z150 F800\nM400\nT1\nM400\nG1 X190 Z150 F8400\nM400")
        self.goto_next_step_stacked_widget()

    def on_measure_right_next_button_clicked(self):
        self._printer.write_gcode_commands(
            "G1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F320\nM400")
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(self.tr("Please enter the absolute value from the dial indicator."),
                                         "dial_indicator_right")
        self._printer.write_gcode_commands("G1 Z150 F800\nM400\nG28X")
        self.goto_next_step_stacked_widget()
        self.finished_handle.next_button.setText(self.tr("Done."))

    def on_finished_next_button_clicked(self):
        self._printer.save_dial_indicator_value()
        self._parent.footer.setEnabled(True)
        self._parent.gotoPreviousPage()

    def reset_message_title(self):
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Preheat extruder."),
            self.tr("Clean the nozzle."),
            self.tr("Place dial indicator."),
            self.tr("Measure compensation value(Left)."),
            self.tr("Measure compensation value(Right)."),
            self.tr("Finish.")
        ]
