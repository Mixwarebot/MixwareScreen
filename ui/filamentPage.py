from qtCore import *
from ui.base.basePushButton import BasePushButton
from ui.base.handleBar import HandleBar
from ui.base.messageBar import MessageBar

work_position = { 'X': 190, 'Y': 20, 'Z': 50 }
load_length = 100
load_speed = 200
load_time = load_length * 60 / load_speed
unload_purge_length = 15
unload_purge_speed = load_speed
unload_length = 100
unload_speed = 1500
unload_time = unload_purge_length * 60 / unload_purge_speed + unload_length * 60 / unload_speed

class FilamentPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent

        self.setObjectName("filamentPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height()/2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.need_preheat = False
        self.step_4_progress = None
        self._backup_target = {
            'left': 0,
            'right': 0
        }
        self.current_filament = None
        self.current_work_mode = None

        self.thermal_frame = QFrame()
        self.thermal_left = QLabel()
        self.thermal_right = QLabel()
        self.thermal_left_button = BasePushButton()
        self.thermal_right_button = BasePushButton()

        self.message_frame = QFrame()
        self.message_text_list = [
            self.tr("Select the extruder."),
            self.tr("Select the work mode."),
            self.tr("Select the filament."),
            self.tr("Wait to heat up."),
            self.tr("Wait for the job to finish."),
            self.tr("Done.")
        ]
        self.message_list = []
        for count in range(len(self.message_text_list)):
            self.message_list.append(MessageBar(count+1, self.message_text_list[count]))

        self.handle_frame = QFrame()
        self.handle_stacked_widget = QStackedWidget()

        self.step_0 = HandleBar()
        self.step_1 = HandleBar()
        self.step_2 = HandleBar()
        self.step_3 = HandleBar()
        self.step_4 = HandleBar()
        self.step_5 = HandleBar()
        self.handle_stacked_widget.addWidget(self.step_0)
        self.handle_stacked_widget.addWidget(self.step_1)
        self.handle_stacked_widget.addWidget(self.step_2)
        self.handle_stacked_widget.addWidget(self.step_3)
        self.handle_stacked_widget.addWidget(self.step_4)
        self.handle_stacked_widget.addWidget(self.step_5)

        self.step_0_left_button = BasePushButton(self.tr("Left"))
        self.step_0_right_button = BasePushButton(self.tr("Right"))

        self.step_1_load_button = BasePushButton(self.tr("Load"))
        self.step_1_unload_button = BasePushButton(self.tr("Unload"))

        self.step_2_pla_button = BasePushButton(self.tr("PLA"))
        self.step_2_abs_button = BasePushButton(self.tr("ABS"))
        self.step_2_pet_button = BasePushButton(self.tr("PET"))
        self.step_2_pa_button = BasePushButton(self.tr("PA"))

        self.step_3_text = QLabel(self.tr("Heating"))

        self.step_4_text = QLabel(self.tr("Working"))
        self.step_4_progress_bar = QProgressBar()
        self.step_4_timer = QTimer()

        self.step_5_text = QLabel(self.tr("Finished"))

        self.initForm()
        self.initLayout()
        self.initConnect()

        self.set_work_mode("Load")
        self.set_filament("PLA")

    def goto_previous_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index > 0:
            self.message_list[index].setEnabled(False)
            self.message_list[index-1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index-1)

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self.message_list[index].setEnabled(False)
            self.message_list[index+1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)
    def on_step_5_next_button_clicked(self):
        self.reset_ui()
        self.recovery_target()
        for i in range(len(self.message_list)):
            self.message_list[i].setEnabled(False)
        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

    def on_step_4_timer_timeout(self):
        self.step_4_progress += 1
        self.step_4_progress_bar.setValue(self.step_4_progress)

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

    def on_step_3_previous_button_clicked(self):
        self.recovery_target()
        self.goto_previous_step_stacked_widget()

    def on_step_3_next_button_clicked(self):
        timer_frame = 2
        if self.current_work_mode == self.tr("Load"):
            self._printer.write_gcode_command(f"G91\nG0\nG1 E{load_length} F{load_speed}\nG90\nM400")
            self.step_4_progress_bar.setMaximum(int(load_time * timer_frame))
        else:
            self._printer.write_gcode_command(f"G91\nG1 E{unload_purge_length} F{unload_purge_speed}\n"
                                              f"G1 E-{unload_length} F{unload_speed}\nG90\nM400")
            self.step_4_progress_bar.setMaximum(int(unload_time * timer_frame))
        self.goto_next_step_stacked_widget()
        self.step_4_progress = 0
        self.step_4_timer.start(int(1000 / timer_frame))

    def set_filament(self, filament: str):
        self.current_filament = filament
        if self.current_filament == "PLA":
            self.step_2_pla_button.setStyleSheet(checkedStyleSheet)
            self.step_2_abs_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_pet_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_pa_button.setStyleSheet(uncheckedStyleSheet)
        elif self.current_filament == "ABS":
            self.step_2_pla_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_abs_button.setStyleSheet(checkedStyleSheet)
            self.step_2_pet_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_pa_button.setStyleSheet(uncheckedStyleSheet)
        elif self.current_filament == "PET":
            self.step_2_pla_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_abs_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_pet_button.setStyleSheet(checkedStyleSheet)
            self.step_2_pa_button.setStyleSheet(uncheckedStyleSheet)
        elif self.current_filament == "PA":
            self.step_2_pla_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_abs_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_pet_button.setStyleSheet(uncheckedStyleSheet)
            self.step_2_pa_button.setStyleSheet(checkedStyleSheet)

    def on_step_2_pla_button_clicked(self):
        self.set_filament("PLA")

    def on_step_2_abs_button_clicked(self):
        self.set_filament("ABS")

    def on_step_2_pet_button_clicked(self):
        self.set_filament("PET")

    def on_step_2_pa_button_clicked(self):
        self.set_filament("PA")

    def on_step_2_previous_button_clicked(self):
        self.goto_previous_step_stacked_widget()

    def on_step_2_next_button_clicked(self):
        self.message_list[2].setText(self.tr("Current filament: {}").format(self.current_filament))
        self.step_3.next_button.setEnabled(False)
        if self.current_filament == "PLA":
            self._printer.set_thermal(self._printer.get_extruder(), 210)
        elif self.current_filament == "ABS":
            self._printer.set_thermal(self._printer.get_extruder(), 250)
        elif self.current_filament == "PET":
            self._printer.set_thermal(self._printer.get_extruder(), 280)
        elif self.current_filament == "PA":
            self._printer.set_thermal(self._printer.get_extruder(), 300)
        self.goto_next_step_stacked_widget()

    def on_step_1_previous_button_clicked(self):
        self.goto_previous_step_stacked_widget()

    def on_step_1_next_button_clicked(self):
        if self._printer.get_position('X') != work_position['X']:
            self._printer.write_gcode_command(f"G1 X{work_position['X']} F6000")
        if self._printer.get_position('Y') != work_position['Y']:
            self._printer.write_gcode_command(f"G1 Y{work_position['Y']} F6000")
        if self._printer.get_position('Z') != work_position['Z']:
            self._printer.write_gcode_command(f"G1 Z{work_position['Z']} F2400")
        self.message_list[1].setText(self.tr("Current work mode: {}").format(self.current_work_mode))
        self.goto_next_step_stacked_widget()

    def set_work_mode(self, mode):
        self.current_work_mode = mode
        if mode == self.tr("Load"):
            self.step_1_load_button.setStyleSheet(checkedStyleSheet)
            self.step_1_unload_button.setStyleSheet(uncheckedStyleSheet)
        else:
            self.step_1_load_button.setStyleSheet(uncheckedStyleSheet)
            self.step_1_unload_button.setStyleSheet(checkedStyleSheet)

    def reset_work_mode(self):
        self.set_work_mode(self.tr("Load"))

    def on_step_1_unload_button_clicked(self):
        self.set_work_mode(self.tr("Unload"))

    def on_step_1_load_button_clicked(self):
        self.set_work_mode(self.tr("Load"))

    def on_step_0_next_button_clicked(self):
        self.message_list[0].setText(f"Current extruder: {self._printer.get_extruder().title()}")
        self.goto_next_step_stacked_widget()

    def on_step_0_right_button_clicked(self):
        if self._printer.get_extruder() != "right":
            self._printer.write_gcode_command('T1')

    def on_step_0_left_button_clicked(self):
        if self._printer.get_extruder() != "left":
            self._printer.write_gcode_command('T0')

    def initForm(self):
        self.thermal_frame.setObjectName("frameBox")
        self.thermal_frame.setFixedHeight(80)
        self.thermal_left.setObjectName("leftLogo")
        self.thermal_right.setObjectName("rightLogo")
        self.thermal_left_button.setText("-")
        self.thermal_left_button.setFixedHeight(40)
        self.thermal_right_button.setText("-")
        self.thermal_right_button.setFixedHeight(40)

        self.message_frame.setObjectName("frameBox")
        self.handle_frame.setObjectName("frameBox")

        self.step_0_left_button.setObjectName("extruderButton")
        self.step_0_right_button.setObjectName("extruderButton")
        self.step_0.previous_button.hide()

        self.step_1_load_button.setObjectName("extruderButton")
        self.step_1_unload_button.setObjectName("extruderButton")

        self.step_2_pla_button.setObjectName("extruderButton")
        self.step_2_abs_button.setObjectName("extruderButton")
        self.step_2_pet_button.setObjectName("extruderButton")
        self.step_2_pa_button.setObjectName("extruderButton")

        self.step_3_text.setAlignment(Qt.AlignCenter)

        self.step_4_text.setAlignment(Qt.AlignCenter)
        self.step_4_progress_bar.setFixedHeight(20)
        self.step_4.footer.hide()

        self.step_5_text.setAlignment(Qt.AlignCenter)
        self.step_5.previous_button.hide()
        self.step_5.next_button.setText(self.tr("Confirm"))

    def initLayout(self):
        thermal_frame_layout = QHBoxLayout(self.thermal_frame)
        thermal_frame_layout.setContentsMargins(20, 20, 20, 20)
        thermal_frame_layout.setSpacing(0)
        thermal_frame_layout.addWidget(self.thermal_left, 1)
        thermal_frame_layout.addWidget(self.thermal_left_button, 3)
        thermal_frame_layout.addWidget(self.thermal_right, 1)
        thermal_frame_layout.addWidget(self.thermal_right_button, 3)

        message_layout = QVBoxLayout(self.message_frame)
        message_layout.setContentsMargins(20, 20, 20, 20)
        message_layout.setSpacing(10)
        for i in range(len(self.message_list)):
            message_layout.addWidget(self.message_list[i])

        step_0_body_layout = QHBoxLayout(self.step_0.body)
        step_0_body_layout.setContentsMargins(0, 0, 0, 0)
        step_0_body_layout.setSpacing(0)
        step_0_body_layout.addWidget(self.step_0_left_button)
        step_0_body_layout.addWidget(self.step_0_right_button)

        step_1_body_layout = QHBoxLayout(self.step_1.body)
        step_1_body_layout.setContentsMargins(0, 0, 0, 0)
        step_1_body_layout.setSpacing(0)
        step_1_body_layout.addWidget(self.step_1_load_button)
        step_1_body_layout.addWidget(self.step_1_unload_button)

        step_2_body_layout = QGridLayout(self.step_2.body)
        step_2_body_layout.setContentsMargins(0, 0, 0, 0)
        step_2_body_layout.setSpacing(0)
        step_2_body_layout.addWidget(self.step_2_pla_button, 0, 0)
        step_2_body_layout.addWidget(self.step_2_abs_button, 0, 1)
        step_2_body_layout.addWidget(self.step_2_pet_button, 1, 0)
        step_2_body_layout.addWidget(self.step_2_pa_button, 1, 1)

        step_3_body_layout = QVBoxLayout(self.step_3.body)
        step_3_body_layout.setContentsMargins(0, 0, 0, 0)
        step_3_body_layout.setSpacing(0)
        step_3_body_layout.addWidget(self.step_3_text)

        step_4_body_layout = QVBoxLayout(self.step_4.body)
        step_4_body_layout.setContentsMargins(0, 0, 0, 0)
        step_4_body_layout.setSpacing(0)
        step_4_body_layout.addWidget(self.step_4_text)
        step_4_body_layout.addWidget(self.step_4_progress_bar)

        step_5_body_layout = QVBoxLayout(self.step_5.body)
        step_5_body_layout.setContentsMargins(0, 0, 0, 0)
        step_5_body_layout.setSpacing(0)
        step_5_body_layout.addWidget(self.step_5_text)

        frame_layout = QVBoxLayout(self.handle_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(10)
        frame_layout.addWidget(self.handle_stacked_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)
        layout.addWidget(self.thermal_frame)
        layout.addWidget(self.message_frame)
        layout.addWidget(self.handle_frame)

    def initConnect(self):
        self._printer.updatePrinterInformation.connect(self.onUpdatePrinterInformation)

        self.thermal_left_button.clicked.connect(self._parent.open_thermal_left_numberPad)
        self.thermal_right_button.clicked.connect(self._parent.open_thermal_right_numberPad)

        self.step_0_left_button.clicked.connect(self.on_step_0_left_button_clicked)
        self.step_0_right_button.clicked.connect(self.on_step_0_right_button_clicked)
        self.step_0.next_button.clicked.connect(self.on_step_0_next_button_clicked)

        self.step_1_load_button.clicked.connect(self.on_step_1_load_button_clicked)
        self.step_1_unload_button.clicked.connect(self.on_step_1_unload_button_clicked)
        self.step_1.previous_button.clicked.connect(self.on_step_1_previous_button_clicked)
        self.step_1.next_button.clicked.connect(self.on_step_1_next_button_clicked)

        self.step_2_pla_button.clicked.connect(self.on_step_2_pla_button_clicked)
        self.step_2_abs_button.clicked.connect(self.on_step_2_abs_button_clicked)
        self.step_2_pet_button.clicked.connect(self.on_step_2_pet_button_clicked)
        self.step_2_pa_button.clicked.connect(self.on_step_2_pa_button_clicked)
        self.step_2.previous_button.clicked.connect(self.on_step_2_previous_button_clicked)
        self.step_2.next_button.clicked.connect(self.on_step_2_next_button_clicked)

        self.step_3.previous_button.clicked.connect(self.on_step_3_previous_button_clicked)
        self.step_3.next_button.clicked.connect(self.on_step_3_next_button_clicked)

        self.step_4_timer.timeout.connect(self.on_step_4_timer_timeout)

        self.step_5.next_button.clicked.connect(self.on_step_5_next_button_clicked)

    def reset_ui(self):
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)

        self.message_list[0].setEnabled(True)
        self.handle_stacked_widget.setCurrentIndex(0)

        self.current_work_mode = self.tr("Load")
        self.current_filament = "PLA"

    @pyqtSlot()
    def onUpdatePrinterInformation(self):
        if self._printer.get_extruder() == "left":
            self.step_0_left_button.setStyleSheet(checkedStyleSheet)
            self.step_0_right_button.setStyleSheet(uncheckedStyleSheet)
        elif self._printer.get_extruder() == "right":
            self.step_0_left_button.setStyleSheet(uncheckedStyleSheet)
            self.step_0_right_button.setStyleSheet(checkedStyleSheet)
        self.thermal_left_button.setText(self._printer.get_thermal('left'))
        self.thermal_right_button.setText(self._printer.get_thermal('right'))

        if self.handle_stacked_widget.currentWidget() == self.step_3 and not self.step_3.next_button.isEnabled():
            if self._printer.get_temperature(self._printer.get_extruder()) + 3 >= self._printer.get_target(self._printer.get_extruder()) > 170:
                self.step_3.next_button.setEnabled(True)
                self.step_3_text.setText(self.tr("Heat completed,\nclick <Next> to start working."))
        elif self.handle_stacked_widget.currentWidget() == self.step_4:
            if self.step_4_progress_bar.value() == self.step_4_progress_bar.maximum():
                self.step_4_progress_bar.setValue(0)
                self.step_4_timer.stop()
                self.goto_next_step_stacked_widget()

    def showEvent(self, a0: QShowEvent) -> None:
        self._printer.write_gcode_command(f"G28O\nG1 Y{work_position['Y']} Z{work_position['Z']} F6000")
        self.reset_ui()
        self.reset_work_mode()

    def hideEvent(self, a0: QHideEvent) -> None:
        self.need_preheat = False
        self.recovery_target()

