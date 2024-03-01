from qtCore import *
from ui.components.base.basePushButton import BasePushButton
from ui.components.handleBar import HandleBar
from ui.components.messageBar import MessageBar


class FilamentPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self.need_move_to_start = None
        self.message_text_list = None
        self._printer = printer
        self._parent = parent

        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("filamentPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_width(), self._printer.config.get_height() - 84 - 128)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.thermal_frame = QFrame()
        self.thermal_frame.setObjectName("frameBox")
        self.thermal_frame.setFixedHeight(80)
        thermal_frame_layout = QHBoxLayout(self.thermal_frame)
        thermal_frame_layout.setContentsMargins(20, 20, 20, 20)
        thermal_frame_layout.setSpacing(0)

        self.thermal_left = QLabel()
        self.thermal_left.setObjectName("leftLogo")
        thermal_frame_layout.addWidget(self.thermal_left, 1)

        self.thermal_left_button = BasePushButton()
        self.thermal_left_button.setText("-")
        self.thermal_left_button.setFixedHeight(40)
        self.thermal_left_button.clicked.connect(self._parent.open_thermal_left_numberPad)
        thermal_frame_layout.addWidget(self.thermal_left_button, 3)

        self.thermal_right = QLabel()
        self.thermal_right.setObjectName("rightLogo")
        thermal_frame_layout.addWidget(self.thermal_right, 1)

        self.thermal_right_button = BasePushButton()
        self.thermal_right_button.setText("-")
        self.thermal_right_button.setFixedHeight(40)
        self.thermal_right_button.clicked.connect(self._parent.open_thermal_right_numberPad)
        thermal_frame_layout.addWidget(self.thermal_right_button, 3)
        self.layout.addWidget(self.thermal_frame)

        self.message_frame = QFrame()
        self.message_frame.setObjectName("frameBox")
        message_layout = QVBoxLayout(self.message_frame)
        message_layout.setContentsMargins(20, 20, 20, 20)
        message_layout.setSpacing(10)

        self.reset_message_text()
        self.message_list = []
        for count in range(len(self.message_text_list)):
            self.message_list.append(MessageBar(count + 1, self.message_text_list[count]))
        for i in range(len(self.message_list)):
            message_layout.addWidget(self.message_list[i])
        self.layout.addWidget(self.message_frame)

        self.handle_frame = QFrame()
        self.handle_frame.setObjectName("frameBox")
        frame_layout = QVBoxLayout(self.handle_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(10)

        self.handle_stacked_widget = QStackedWidget()

        self.extruder_handle = HandleBar()
        self.extruder_handle.next_button.clicked.connect(self.on_extruder_next_button_clicked)
        extruder_body_layout = QHBoxLayout(self.extruder_handle.body)
        extruder_body_layout.setContentsMargins(0, 0, 0, 0)
        extruder_body_layout.setSpacing(0)
        self.extruder_left_button = BasePushButton()
        self.extruder_left_button.setObjectName("extruderButton")
        self.extruder_left_button.clicked.connect(self.on_extruder_left_button_clicked)
        extruder_body_layout.addWidget(self.extruder_left_button)
        self.extruder_right_button = BasePushButton()
        self.extruder_right_button.setObjectName("extruderButton")
        self.extruder_right_button.clicked.connect(self.on_extruder_right_button_clicked)
        extruder_body_layout.addWidget(self.extruder_right_button)
        self.extruder_handle.previous_button.hide()
        self.handle_stacked_widget.addWidget(self.extruder_handle)

        self.work_mode_handle = HandleBar()
        self.work_mode_handle.previous_button.clicked.connect(self.on_work_mode_previous_button_clicked)
        self.work_mode_handle.next_button.clicked.connect(self.on_work_mode_next_button_clicked)
        work_mode_body_layout = QHBoxLayout(self.work_mode_handle.body)
        work_mode_body_layout.setContentsMargins(0, 0, 0, 0)
        work_mode_body_layout.setSpacing(0)
        self.work_mode_load_button = BasePushButton()
        self.work_mode_load_button.setObjectName("extruderButton")
        self.work_mode_load_button.clicked.connect(self.on_work_mode_load_button_clicked)
        work_mode_body_layout.addWidget(self.work_mode_load_button)
        self.work_mode_unload_button = BasePushButton()
        self.work_mode_unload_button.setObjectName("extruderButton")
        self.work_mode_unload_button.clicked.connect(self.on_work_mode_unload_button_clicked)
        work_mode_body_layout.addWidget(self.work_mode_unload_button)
        self.handle_stacked_widget.addWidget(self.work_mode_handle)

        self.filament_handle = HandleBar()
        self.filament_handle.previous_button.clicked.connect(self.on_filament_previous_button_clicked)
        self.filament_handle.next_button.clicked.connect(self.on_filament_next_button_clicked)
        filament_body_layout = QGridLayout(self.filament_handle.body)
        filament_body_layout.setContentsMargins(0, 0, 0, 0)
        filament_body_layout.setSpacing(0)
        self.filament_pla_button = BasePushButton()
        self.filament_pla_button.setObjectName("extruderButton")
        self.filament_pla_button.clicked.connect(self.on_filament_pla_button_clicked)
        filament_body_layout.addWidget(self.filament_pla_button, 0, 0)
        self.filament_abs_button = BasePushButton()
        self.filament_abs_button.setObjectName("extruderButton")
        self.filament_abs_button.clicked.connect(self.on_filament_abs_button_clicked)
        filament_body_layout.addWidget(self.filament_abs_button, 0, 1)
        self.filament_pet_button = BasePushButton()
        self.filament_pet_button.setObjectName("extruderButton")
        self.filament_pet_button.clicked.connect(self.on_filament_pet_button_clicked)
        filament_body_layout.addWidget(self.filament_pet_button, 1, 0)
        self.filament_pa_button = BasePushButton()
        self.filament_pa_button.setObjectName("extruderButton")
        self.filament_pa_button.clicked.connect(self.on_filament_pa_button_clicked)
        filament_body_layout.addWidget(self.filament_pa_button, 1, 1)
        self.handle_stacked_widget.addWidget(self.filament_handle)

        self.heating_handle = HandleBar()
        self.heating_handle.previous_button.clicked.connect(self.on_heating_previous_button_clicked)
        self.heating_handle.next_button.clicked.connect(self.on_heating_next_button_clicked)
        heating_body_layout = QVBoxLayout(self.heating_handle.body)
        heating_body_layout.setContentsMargins(0, 0, 0, 0)
        heating_body_layout.setSpacing(0)
        self.heating_text = QLabel()
        self.heating_text.setAlignment(Qt.AlignCenter)
        heating_body_layout.addWidget(self.heating_text)
        self.handle_stacked_widget.addWidget(self.heating_handle)

        self.working_handle = HandleBar()
        self.working_handle.footer.hide()
        working_body_layout = QVBoxLayout(self.working_handle.body)
        working_body_layout.setContentsMargins(0, 0, 0, 0)
        working_body_layout.setSpacing(0)
        self.working_text = QLabel()
        self.working_text.setAlignment(Qt.AlignCenter)
        working_body_layout.addWidget(self.working_text)
        self.working_progress_bar = QProgressBar()
        self.working_progress_bar.setFixedHeight(18)
        working_body_layout.addWidget(self.working_progress_bar)
        self.working_timer = QTimer()
        self.working_timer.timeout.connect(self.on_working_timer_timeout)
        self.handle_stacked_widget.addWidget(self.working_handle)

        self.finished_handle = HandleBar()
        self.finished_handle.previous_button.hide()
        self.finished_handle.next_button.clicked.connect(self.on_finished_next_button_clicked)
        finished_body_layout = QVBoxLayout(self.finished_handle.body)
        finished_body_layout.setContentsMargins(0, 0, 0, 0)
        finished_body_layout.setSpacing(0)
        self.finished_text = QLabel()
        self.finished_text.setAlignment(Qt.AlignCenter)
        finished_body_layout.addWidget(self.finished_text)
        self.handle_stacked_widget.addWidget(self.finished_handle)
        frame_layout.addWidget(self.handle_stacked_widget)
        self.layout.addWidget(self.handle_frame)

        self.need_preheat = False
        self.working_progress = None
        self._backup_target = {
            'left': 0,
            'right': 0
        }
        self.current_filament = None
        self.current_work_mode = None

    def showEvent(self, a0: QShowEvent) -> None:
        self.need_move_to_start = True
        self.reset_ui()

    def hideEvent(self, a0: QHideEvent) -> None:
        self.need_preheat = False
        self.recovery_target()

    def reset_message_text(self):
        self.message_text_list = [
            self.tr("Select Extruder"),
            self.tr("Select Working Mode"),
            self.tr("Select Filament"),
            self.tr("Heated Extruder"),
            self.tr("Working"),
            self.tr("Done")
        ]

    def reset_ui(self):
        self.reset_message_text()
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)

        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

        self.extruder_left_button.setText(self.tr("Left"))
        self.extruder_right_button.setText(self.tr("Right"))
        self.work_mode_load_button.setText(self.tr("Load"))
        self.work_mode_unload_button.setText(self.tr("Unload"))
        self.filament_pla_button.setText("PLA")
        self.filament_abs_button.setText("ABS")
        self.filament_pet_button.setText("PET")
        self.filament_pa_button.setText("PA")
        self.heating_text.setText(self.tr("The extruder is heating, please wait."))
        self.working_text.setText(self.tr("Working"))
        self.finished_text.setText(self.tr("Finished"))

        self.reset_work_mode()
        self.reset_filament()

    def goto_previous_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index > 0:
            self.message_list[index].setEnabled(False)
            self.message_list[index - 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index - 1)

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)

    def on_finished_next_button_clicked(self):
        self.reset_ui()
        self.recovery_target()
        for i in range(len(self.message_list)):
            self.message_list[i].setEnabled(False)
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def on_working_timer_timeout(self):
        self.working_progress += 1
        self.working_progress_bar.setValue(self.working_progress)
        if self.handle_stacked_widget.currentWidget() == self.working_handle:
            if self.working_progress_bar.value() >= self.working_progress_bar.maximum():
                self.working_timer.stop()
                self._parent.footer.setEnabled(True)
                self.goto_next_step_stacked_widget()
                self.finished_handle.next_button.setText(self.tr("Confirm"))
                self.working_progress_bar.setValue(0)

    def backup_target(self):
        self._backup_target['left'] = self._printer.get_target('left')
        self._backup_target['right'] = self._printer.get_target('right')

    def recovery_target(self):
        if self.need_preheat:
            self._printer.set_thermal('left', 170)
            self._printer.set_thermal('right', 170)
        else:
            self._printer.set_thermal('left', self._backup_target['left'])
            self._printer.set_thermal('right', self._backup_target['right'])

    def on_heating_previous_button_clicked(self):
        self.recovery_target()
        self.goto_previous_step_stacked_widget()

    def on_heating_next_button_clicked(self):
        timer_frame = 2
        if self.current_work_mode == self.tr("Load"):
            self._printer.write_gcode_command(f"G91\nG0\nG1 E{load_length} F{load_speed}\nG90")
            self.working_progress_bar.setMaximum(int(load_time * timer_frame))
        else:
            self._printer.write_gcode_command(f"G91\nG1 E{unload_purge_length} F{unload_purge_speed}\n"
                                              f"G1 E-{unload_length} F{unload_speed}\nG90")
            self.working_progress_bar.setMaximum(int(unload_time * timer_frame))
        self.goto_next_step_stacked_widget()
        self._parent.footer.setEnabled(False)
        self.working_progress = 0
        self.working_timer.start(int(1000 / timer_frame))

    def set_filament(self, filament: str):
        self.current_filament = filament
        if self.current_filament == "PLA":
            update_style(self.filament_pla_button, "checked")
            update_style(self.filament_abs_button, "unchecked")
            update_style(self.filament_pet_button, "unchecked")
            update_style(self.filament_pa_button, "unchecked")
        elif self.current_filament == "ABS":
            update_style(self.filament_pla_button, "unchecked")
            update_style(self.filament_abs_button, "checked")
            update_style(self.filament_pet_button, "unchecked")
            update_style(self.filament_pa_button, "unchecked")
        elif self.current_filament == "PET":
            update_style(self.filament_pla_button, "unchecked")
            update_style(self.filament_abs_button, "unchecked")
            update_style(self.filament_pet_button, "checked")
            update_style(self.filament_pa_button, "unchecked")
        elif self.current_filament == "PA":
            update_style(self.filament_pla_button, "unchecked")
            update_style(self.filament_abs_button, "unchecked")
            update_style(self.filament_pet_button, "unchecked")
            update_style(self.filament_pa_button, "checked")

    def reset_filament(self):
        self.set_filament("PLA")

    def on_filament_pla_button_clicked(self):
        self.set_filament("PLA")

    def on_filament_abs_button_clicked(self):
        self.set_filament("ABS")

    def on_filament_pet_button_clicked(self):
        self.set_filament("PET")

    def on_filament_pa_button_clicked(self):
        self.set_filament("PA")

    def on_filament_previous_button_clicked(self):
        self.goto_previous_step_stacked_widget()

    def on_filament_next_button_clicked(self):
        self.message_list[2].setText(self.tr("Current filament: {}").format(self.current_filament))
        self.heating_text.setText(self.tr("The extruder is heating, please wait."))
        self.heating_handle.next_button.setEnabled(False)
        if self.current_filament == "PLA":
            self._printer.set_thermal(self._printer.get_extruder(), 210)
        elif self.current_filament == "ABS":
            self._printer.set_thermal(self._printer.get_extruder(), 250)
        elif self.current_filament == "PET":
            self._printer.set_thermal(self._printer.get_extruder(), 280)
        elif self.current_filament == "PA":
            self._printer.set_thermal(self._printer.get_extruder(), 300)
        self.goto_next_step_stacked_widget()

    def on_work_mode_previous_button_clicked(self):
        self.goto_previous_step_stacked_widget()

    def on_work_mode_next_button_clicked(self):
        self.message_list[1].setText(self.tr("Current work mode: {}").format(self.current_work_mode))
        self.goto_next_step_stacked_widget()

    def set_work_mode(self, mode):
        self.current_work_mode = mode
        if mode == self.tr("Load"):
            update_style(self.work_mode_load_button, "checked")
            update_style(self.work_mode_unload_button, "unchecked")
        else:
            update_style(self.work_mode_load_button, "unchecked")
            update_style(self.work_mode_unload_button, "checked")

    def reset_work_mode(self):
        self.set_work_mode(self.tr("Load"))

    def on_work_mode_unload_button_clicked(self):
        self.set_work_mode(self.tr("Unload"))

    def on_work_mode_load_button_clicked(self):
        self.set_work_mode(self.tr("Load"))

    def move_to_start_position(self):
        if self.need_move_to_start:
            self._printer.write_gcode_command("M155 S1")
            self._printer.auto_home()
            if not self._printer.is_printing():
                self._printer.move_to_z(filament_position['Z'])
            self._printer.move_to_xy(filament_position['X'], filament_position['Y'], True)
            self._printer.write_gcode_command("M155 S0")
            self.need_move_to_start = False

    def on_extruder_next_button_clicked(self):
        self.move_to_start_position()
        if self._printer.get_extruder() == "left":
            self.message_list[0].setText(self.tr("Current extruder: Left."))
        elif self._printer.get_extruder() == "right":
            self.message_list[0].setText(self.tr("Current extruder: Right."))
        self.goto_next_step_stacked_widget()

    def on_extruder_right_button_clicked(self):
        self.move_to_start_position()
        if self._printer.get_extruder() != "right":
            self._printer.write_gcode_command('T1')

    def on_extruder_left_button_clicked(self):
        self.move_to_start_position()
        if self._printer.get_extruder() != "left":
            self._printer.write_gcode_command('T0')

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        if self._printer.get_extruder() == "left":
            update_style(self.extruder_left_button, "checked")
            update_style(self.extruder_right_button, "unchecked")
        elif self._printer.get_extruder() == "right":
            update_style(self.extruder_left_button, "unchecked")
            update_style(self.extruder_right_button, "checked")

        self.thermal_left_button.setText(self._printer.get_thermal('left'))
        self.thermal_right_button.setText(self._printer.get_thermal('right'))

        if self.handle_stacked_widget.currentWidget() == self.heating_handle and not self.heating_handle.next_button.isEnabled():
            if self._printer.get_temperature(self._printer.get_extruder()) + 3 >= self._printer.get_target(
                    self._printer.get_extruder()) > 170:
                self.heating_handle.next_button.setEnabled(True)
                self.heating_text.setText(self.tr("Heat completed,\nclick <Next> to start working."))
