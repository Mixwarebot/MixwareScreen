from enum import Enum, auto

from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.components.baseTitleFrame import BaseTitleFrame
from ui.components.handleBar import HandleBar
from ui.components.movieLabel import MovieLabel


class ProbeTargetStatus(Enum):
    XYOC_STATE_CLEAN = auto()
    XYOC_STATE_PLACE_X = auto()
    XYOC_STATE_MEASURING_X = auto()
    XYOC_STATE_PLACE_Y = auto()
    XYOC_STATE_MEASURING_Y = auto()
    XYOC_STATE_CALCULATE = auto()
    XYOC_STATE_SAVE = auto()
    XYOC_STATE_ERROR = auto()


xyoc_measure_count = 1
xyoc_feedrate_travel = 6000
xyoc_feedrate_travel_z = 1200
xyoc_start_pos_x = {
    'X': 208,  # Measure the starting point.(x)
    'Y': 0,  # Measure the starting point.(y)
}
xyoc_start_pos_y = {
    'X': 190,  # Measure the starting point.(x)
    'Y': 88,  # Measure the starting point.(y)
}
xyoc_start_pos_z = 45  # Measure the placement height of the tool.(z)


class XYOffsetsCalibratorPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._offsets_x = None
        self._offsets_y = None
        self._state = ProbeTargetStatus.XYOC_STATE_CLEAN
        self._printer = printer
        self._printer.endstops_hit.connect(self.on_endstops_hit)
        self._parent = parent
        self.message_text_list = None

        self.setObjectName("XYOffsetsCalibratorPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.reset_message_text()
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
        self.handle_frame_layout.addWidget(self.handle_stacked_widget)
        self.layout.addWidget(self.handle_frame)

        self.tips_handle = HandleBar()
        self.tips_handle.previous_button.hide()
        self.tips_handle.next_button.clicked.connect(self.on_tips_next_button_clicked)
        self.tips_layout = QVBoxLayout(self.tips_handle.body)
        self.tips_layout.setContentsMargins(20, 0, 20, 0)
        self.tips_layout.setSpacing(0)
        self.tips_layout.setAlignment(Qt.AlignCenter)
        self.tips_logo = MovieLabel("resource/image/clean_bed.gif", 320, 320)
        self.tips_logo.setFixedSize(320, 320)
        self.tips_layout.addWidget(self.tips_logo)
        self.tips_text = QLabel()
        self.tips_text.setWordWrap(True)
        self.tips_text.setAlignment(Qt.AlignCenter)
        self.tips_layout.addWidget(self.tips_text)
        self.handle_stacked_widget.addWidget(self.tips_handle)

        self.place_handle = HandleBar()
        self.place_handle.previous_button.hide()
        self.place_handle.next_button.clicked.connect(self.on_place_next_button_clicked)
        self.place_layout = QVBoxLayout(self.place_handle.body)
        self.place_layout.setContentsMargins(20, 0, 20, 0)
        self.place_layout.setSpacing(0)
        self.place_layout.setAlignment(Qt.AlignCenter)
        self.place_x_logo = QLabel()
        self.place_x_logo.setFixedHeight(320)
        self.place_x_logo.setAlignment(Qt.AlignCenter)
        self.place_x_logo.setPixmap(QPixmap("resource/image/xyoc_x").scaledToWidth(320))
        self.place_layout.addWidget(self.place_x_logo)
        self.place_y_logo = QLabel()
        self.place_y_logo.setFixedHeight(320)
        self.place_y_logo.setAlignment(Qt.AlignCenter)
        self.place_y_logo.setPixmap(QPixmap("resource/image/xyoc_y").scaledToWidth(320))
        self.place_layout.addWidget(self.place_y_logo)
        self.place_text = QLabel()
        self.place_text.setWordWrap(True)
        self.place_text.setAlignment(Qt.AlignCenter)
        self.place_layout.addWidget(self.place_text)
        self.handle_stacked_widget.addWidget(self.place_handle)

        self.work_handle = HandleBar()
        self.work_handle.footer.hide()
        self.work_layout = QVBoxLayout(self.work_handle.body)
        self.work_layout.setContentsMargins(20, 0, 20, 0)
        self.work_layout.setSpacing(0)
        self.work_layout.setAlignment(Qt.AlignCenter)
        self.work_load = MovieLabel("resource/image/loading.gif", 48, 48)
        self.work_load.setFixedHeight(64)
        self.work_layout.addWidget(self.work_load)
        self.work_text = QLabel()
        self.work_text.setWordWrap(True)
        self.work_text.setAlignment(Qt.AlignCenter)
        self.work_layout.addWidget(self.work_text)
        self.handle_stacked_widget.addWidget(self.work_handle)

        self.finish_handle = HandleBar()
        self.finish_handle.previous_button.hide()
        self.finish_handle.next_button.clicked.connect(self.on_finished_next_button_clicked)
        self.finish_layout = QVBoxLayout(self.finish_handle.body)
        self.finish_layout.setContentsMargins(20, 0, 20, 0)
        self.finish_layout.setSpacing(0)
        self.finish_text = QLabel()
        self.finish_text.setFixedHeight(128)
        self.finish_text.setWordWrap(True)
        self.finish_text.setAlignment(Qt.AlignCenter)
        self.finish_layout.addWidget(self.finish_text)
        self.finish_reset_button = BasePushButton()
        self.finish_reset_button.setFixedHeight(64)
        self.finish_reset_button.clicked.connect(self.on_reset_button_clicked)
        self.finish_layout.addWidget(self.finish_reset_button)
        self.handle_stacked_widget.addWidget(self.finish_handle)

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def hideEvent(self, a0):
        self._printer.xy_probe_target(False)

    def reset_message_text(self):
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Place xy calibrator."),
            self.tr("Measuring."),
            self.tr("Finish."),
        ]

    def reset_ui(self):
        self.reset_message_text()
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
            self.message_list[count].show() if count < 3 else self.message_list[count].hide()
        self.place_x_logo.show()
        self.place_y_logo.hide()
        self.finish_reset_button.hide()
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)
        self.finish_handle.footer.setEnabled(True)
        self._printer.xy_probe_target(False)
        self._state = ProbeTargetStatus.XYOC_STATE_CLEAN

    def re_translate_ui(self):
        self.tips_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.place_text.setText(
            self.tr("Please place the xy calibrator at the designated location and connect the cable."))
        self.work_text.setText(self.tr("Measuring, please wait."))
        self.finish_text.setText(self.tr("Measure completed."))
        self.finish_reset_button.setText(self.tr("Reset offsets and Remeasure"))

    @pyqtSlot(str, float)
    def on_endstops_hit(self, axis, position):
        self._parent.footer.setEnabled(True)
        if axis in ['X', 'Y']:
            if self._state == ProbeTargetStatus.XYOC_STATE_MEASURING_X:
                self._offsets_x = float('%.2f' % position)
                self._state = ProbeTargetStatus.XYOC_STATE_PLACE_Y
                self.place_x_logo.hide()
                self.place_y_logo.show()
                self.on_tips_next_button_clicked()
            elif self._state == ProbeTargetStatus.XYOC_STATE_MEASURING_Y:
                self._offsets_y = float('%.2f' % position)
                self._state = ProbeTargetStatus.XYOC_STATE_CALCULATE
                self.goto_next_step_stacked_widget()
                self.handle_stacked_widget.currentWidget().setEnabled(True)
                self._parent.footer.setEnabled(True)
                self.finish_handle.next_button.setText(self.tr("Save"))

                if abs(self._offsets_x) > 3 or abs(self._offsets_y) > 2:
                    self._state = ProbeTargetStatus.XYOC_STATE_ERROR
                    self.finish_text.setText(self.tr("Unusual measurement data!\nPlease recalibrate."))
                    self.finish_handle.footer.setEnabled(False)
                    self.finish_reset_button.show()
                    self._parent.showShadowScreen()
                    self._parent.message.start("Mixware Screen",
                                               self.tr("Unusual measurement data!\nPlease recalibrate."),
                                               buttons=QMessageBox.Yes)
                    self._parent.closeShadowScreen()
                else:
                    ox = float('%.2f' %
                               (self._printer.information['probe']['offset']['right']['X'] + self._offsets_x))
                    oy = float('%.2f' %
                               (self._printer.information['probe']['offset']['right']['Y'] + self._offsets_y))
                    a0 = self.tr("Measure completed.") + f"\n\nX: {ox}({self._offsets_x})\nY: {oy}({self._offsets_y})"
                    self.finish_text.setText(a0)

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

    def on_tips_next_button_clicked(self):
        self._printer.write_gcode_commands(
            F"G28\n"
            F"T0\n"
            F"G1 Z{xyoc_start_pos_z} F{xyoc_feedrate_travel_z}\n"
        )
        if self._state == ProbeTargetStatus.XYOC_STATE_CLEAN:
            self._state = ProbeTargetStatus.XYOC_STATE_PLACE_X
            self.goto_next_step_stacked_widget()
            self._printer.write_gcode_commands(
                F"G1 X{xyoc_start_pos_x['X']} Y{xyoc_start_pos_x['Y']} F{xyoc_feedrate_travel}\n"
            )
        elif self._state == ProbeTargetStatus.XYOC_STATE_PLACE_Y:
            self.goto_previous_step_stacked_widget()
            self._parent.footer.setEnabled(True)
            self._printer.write_gcode_commands(
                F"G1 X{xyoc_start_pos_y['X']} Y{xyoc_start_pos_y['Y']} F{xyoc_feedrate_travel}\n"
            )

    def on_place_next_button_clicked(self):
        if is_release:
            self._parent.footer.setEnabled(False)
        self.goto_next_step_stacked_widget()

        self._printer.xy_probe_target()
        if self._state == ProbeTargetStatus.XYOC_STATE_PLACE_X:
            self._state = ProbeTargetStatus.XYOC_STATE_MEASURING_X
            self._printer.write_gcode_commands(F"G429XC{xyoc_measure_count}")
        elif self._state == ProbeTargetStatus.XYOC_STATE_PLACE_Y:
            self._state = ProbeTargetStatus.XYOC_STATE_MEASURING_Y
            self._printer.write_gcode_commands(F"G429YC{xyoc_measure_count}")

    def on_finished_next_button_clicked(self):
        self._state = ProbeTargetStatus.XYOC_STATE_SAVE
        self._printer.set_hotend_offset('X', self._printer.information['probe']['offset']['right']['X'] + float(
            self._offsets_x))
        self._printer.set_hotend_offset('Y', self._printer.information['probe']['offset']['right']['Y'] + float(
            self._offsets_y))
        self._parent.gotoPreviousPage()

    def on_reset_button_clicked(self):
        self.reset_ui()
        self.re_translate_ui()
        self._printer.set_hotend_offset('X', 385, False)
        self._printer.set_hotend_offset('Y', 0, False)
