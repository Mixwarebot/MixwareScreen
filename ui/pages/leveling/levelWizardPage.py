from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.components.base.baseLine import BaseHLine, BaseVLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.handleBar import HandleBar
from ui.components.messageBar import MessageBar
from ui.components.leveling.bedMeshGraph import BedMeshGraph


class LevelWizardPage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self.message_text_list = None
        self._printer = printer
        self._parent = parent
        self.offset = {
            'left': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
            'right': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        }

        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("levelWizardPage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        self.message_frame = QFrame()
        self.message_frame.setObjectName("frameBox")
        self.message_frame.setFixedSize(360, 240)
        self.message_layout = QVBoxLayout(self.message_frame)
        self.message_layout.setContentsMargins(20, 20, 20, 20)
        self.message_layout.setSpacing(10)
        self.message_list = []
        self.reset_message_title()
        for i in range(len(self.message_text_list)):
            self.message_list.append(MessageBar(i + 1, self.message_text_list[i]))
            self.message_layout.addWidget(self.message_list[i])
        self.layout.addWidget(self.message_frame)

        self.start_frame = QFrame()
        self.start_frame_layout = QVBoxLayout(self.start_frame)
        self.start_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.start_frame_layout.setSpacing(10)
        self.start_frame_layout.setAlignment(Qt.AlignCenter)
        self.bed_mesh_graph = BedMeshGraph()
        self.start_frame_layout.addWidget(self.bed_mesh_graph)
        self.start_button = BasePushButton()
        self.start_button.setFixedSize(360, 64)
        self.start_button.clicked.connect(self.on_start_button_clicked)
        self.start_frame_layout.addWidget(self.start_button)
        self.layout.addWidget(self.start_frame)

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
        # self.remind_logo.setPixmap(QPixmap("resource/image/level_clean_bed.png"))
        self.remind_logo_movie = QMovie("resource/image/clean_bed.gif")
        self.remind_logo_movie.setScaledSize(self.remind_logo.size())
        self.remind_logo.setMovie(self.remind_logo_movie)
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
        self.clean_timer = QTimer()
        self.clean_timer.timeout.connect(self.on_clean_timer_timeout)
        self.clean_handle.next_button.clicked.connect(self.on_clean_next_button_clicked)
        self.clean_body_layout = QVBoxLayout(self.clean_handle.body)
        self.clean_body_layout.setContentsMargins(20, 0, 20, 0)
        self.clean_body_layout.setSpacing(0)
        self.clean_body_layout.setAlignment(Qt.AlignCenter)
        self.clean_logo = QLabel()
        self.clean_logo.setFixedSize(320, 220)
        self.clean_logo_movie = QMovie("resource/image/clean_nozzle.gif")
        self.clean_logo_movie.setScaledSize(self.clean_logo.size())
        self.clean_logo.setMovie(self.clean_logo_movie)
        self.clean_body_layout.addWidget(self.clean_logo)
        self.clean_text = QLabel()
        self.clean_text.setWordWrap(True)
        self.clean_text.setAlignment(Qt.AlignCenter)
        self.clean_body_layout.addWidget(self.clean_text)
        self.handle_stacked_widget.addWidget(self.clean_handle)

        self.level_handle = HandleBar()
        self.level_handle.previous_button.hide()
        self.level_handle.next_button.clicked.connect(self.on_level_next_button_clicked)
        self.level_body_layout = QVBoxLayout(self.level_handle.body)
        self.level_body_layout.setContentsMargins(19, 0, 20, 0)
        self.level_body_layout.setSpacing(0)
        self.level_body_layout.setAlignment(Qt.AlignCenter)
        self.level_load = QLabel()
        self.level_load.setFixedSize(320, 120)
        self.level_load.setAlignment(Qt.AlignCenter)
        self.level_body_layout.addWidget(self.level_load)
        self.level_mesh_graph = BedMeshGraph()
        self.level_mesh_graph.body_frame.setFixedSize(320, 320)
        self.level_body_layout.addWidget(self.level_mesh_graph)
        self.level_text = QLabel()
        self.level_text.setWordWrap(True)
        self.level_text.setAlignment(Qt.AlignCenter)
        self.level_body_layout.addWidget(self.level_text)
        self.handle_stacked_widget.addWidget(self.level_handle)

        self.level_load_rotate = 0
        self.level_load_timer = QTimer()
        self.level_load_timer.timeout.connect(self.on_level_load_timer_timeout)

        self.offset_handle = HandleBar()
        self.offset_handle.previous_button.hide()
        self.offset_handle.next_button.clicked.connect(self.on_offset_next_button_clicked)
        self.offset_body_layout = QVBoxLayout(self.offset_handle.body)
        self.offset_body_layout.setContentsMargins(20, 0, 20, 0)
        self.offset_body_layout.setSpacing(0)
        self.offset_logo = QLabel()
        self.offset_logo.setFixedSize(320, 320)
        self.offset_logo_movie = QMovie("resource/image/adjust_offset.gif")
        self.offset_logo_movie.setScaledSize(self.offset_logo.size())
        self.offset_logo.setMovie(self.offset_logo_movie)
        self.offset_body_layout.addWidget(self.offset_logo)
        self.offset_text = QLabel()
        self.offset_text.setWordWrap(True)
        self.offset_text.setAlignment(Qt.AlignCenter)
        self.offset_body_layout.addWidget(self.offset_text)
        self.offset_distance_frame = QFrame()
        self.offset_distance_frame.setFixedHeight(128)
        self.distance_layout = QVBoxLayout(self.offset_distance_frame)
        self.distance_layout.setContentsMargins(0, 0, 0, 0)
        self.distance_layout.setSpacing(0)
        self.offset_distance_title = QLabel()
        self.offset_distance_title.setObjectName("frame_title")
        self.offset_distance_title.setFixedHeight(40)
        self.distance_layout.addWidget(self.offset_distance_title)
        self.offset_distance_button_frame = QFrame()
        self.offset_distance_button_frame.setObjectName("frameBox")
        self.offset_distance_button_frame.setFixedHeight(88)
        self.distance_frame_layout = QHBoxLayout(self.offset_distance_button_frame)
        self.distance_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.distance_frame_layout.setSpacing(0)
        self.offset_button_group = QButtonGroup()
        self.offset_button_group.buttonClicked.connect(self.on_offset_distance_button_clicked)
        self.offset_distance_list = ["0.01", "0.05", "0.1", "0.5", "1"]
        self.offset_distance_default = "0.1"
        self.offset_distance_current_id = 0
        for d in range(len(self.offset_distance_list)):
            button = BasePushButton()
            button.setText(self.offset_distance_list[d])
            button.setObjectName("dataButton")
            self.offset_button_group.addButton(button, d)
            if self.offset_distance_list[d] == self.offset_distance_default:
                self.on_offset_distance_button_clicked(self.offset_button_group.button(d))
            self.distance_frame_layout.addWidget(button)
        self.distance_layout.addWidget(self.offset_distance_button_frame)
        self.offset_body_layout.addWidget(self.offset_distance_frame)
        self.offset_frame_layout = QVBoxLayout()
        self.offset_frame_layout.setContentsMargins(0, 10, 0, 10)
        self.offset_frame_layout.setSpacing(0)
        self.offset_button_title = QLabel()
        self.offset_button_title.setFixedHeight(40)
        self.offset_button_title.setObjectName("frame_title")
        self.offset_frame_layout.addWidget(self.offset_button_title)
        self.offset_button_frame = QFrame()
        self.offset_button_frame.setFixedHeight(216)
        self.offset_button_frame.setObjectName("frameBox")
        self.offset_button_frame_layout = QVBoxLayout(self.offset_button_frame)
        self.offset_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.offset_button_frame_layout.setSpacing(0)
        self.offset_button_up = BasePushButton()
        self.offset_button_up.setObjectName("upLogo")
        self.offset_button_up.clicked.connect(self.on_offset_button_up_clicked)
        self.offset_button_frame_layout.addWidget(self.offset_button_up)
        self.offset_button_up_label = QLabel()
        self.offset_button_up_label.setFixedHeight(44)
        self.offset_button_up_label.setAlignment(Qt.AlignCenter)
        self.offset_button_frame_layout.addWidget(self.offset_button_up_label)
        self.offset_button_frame_layout.addWidget(BaseHLine())
        self.offset_button_down = BasePushButton()
        self.offset_button_down.setObjectName("downLogo")
        self.offset_button_down.clicked.connect(self.on_offset_button_down_clicked)
        self.offset_button_frame_layout.addWidget(self.offset_button_down)
        self.offset_button_down_label = QLabel()
        self.offset_button_down_label.setFixedHeight(44)
        self.offset_button_down_label.setAlignment(Qt.AlignCenter)
        self.offset_button_frame_layout.addWidget(self.offset_button_down_label)
        self.offset_frame_layout.addWidget(self.offset_button_frame)
        self.offset_body_layout.addLayout(self.offset_frame_layout)
        self.handle_stacked_widget.addWidget(self.offset_handle)

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

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def hideEvent(self, a0: QHideEvent) -> None:
        self.place_logo_movie.stop()
        self.measure_left_logo_movie.stop()
        self.measure_right_logo_movie.stop()

    def reset_message_title(self):
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Preheat extruder."),
            self.tr("Clean the nozzle."),
            self.tr("Auto bed leveling."),
            self.tr("Adjust offset."),
            self.tr("Place dial indicator."),
            self.tr("Measure compensation value(Left)."),
            self.tr("Measure compensation value(Right)."),
            self.tr("Finish.")
        ]

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
        self.message_frame.hide()
        self.bed_mesh_graph.show_bed_mesh(self._printer.information['bedMesh'])
        self.start_frame.show()
        self.handle_stacked_widget.setCurrentIndex(0)
        self.handle_frame.hide()

    def re_translate_ui(self):
        self.start_button.setText(self.tr("Start Auto-leveling"))
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
        self.level_text.setText(self.tr("Auto-leveling, please wait."))
        self.offset_text.setText(self.tr("Adjust offset."))
        self.offset_distance_title.setText(self.tr("Move Distance (mm)"))
        self.offset_button_title.setText("Z: -")
        self.place_text.setText(self.tr("Place the dial indicator at the specified location."))
        self.measure_left_text.setText(self.tr("Click <Next> to start measure compensation value(Left)."))
        self.measure_right_text.setText(self.tr("Click <Next> to start measure compensation value(Right)."))
        self.finished_text.setText(self.tr("Leveling wizard completed."))
        self.offset_button_up_label.setText(self.tr("Lift Bed"))
        self.offset_button_down_label.setText(self.tr("Drop Bed"))

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, state):
        if not self.isVisible():
            return
        if state == MixwareScreenPrinterStatus.PRINTER_G29:
            self.level_handle.next_button.setEnabled(True)
            self.level_text.setText(self.tr("Auto-leveling completed."))
            self.level_load_timer.stop()
            self.level_load.hide()
            self.level_mesh_graph.show_bed_mesh(self._printer.information['bedMesh'])
            self.level_mesh_graph.show()

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return
        self.preheat_thermal_left_button.setText(self._printer.get_thermal('left'))
        self.preheat_thermal_right_button.setText(self._printer.get_thermal('right'))

        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 170 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170:
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))

    @pyqtSlot()
    def on_start_button_clicked(self):
        self.start_frame.hide()
        self.message_frame.show()
        self.handle_frame.show()
        self.remind_logo_movie.start()

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
        self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        self.remind_logo_movie.stop()
        update_style(self.preheat_pla, "unchecked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")
        # preheat -> 170, 170
        # self._printer.write_gcode_commands("M155 S1\nM104 S170 T0\nM104 S170 T1\nG28\nT0\nG1 X0 Y20 Z50 F8400\nM155 S0")
        self._printer.write_gcode_command("T0\nM155 S1\nM104 S170 T0\nM104 S170 T1")
        self._printer.auto_home()
        self._printer.move_to_xy(0, 20, True)
        self._printer.move_to_z(50, True)
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

    def on_preheat_pla_clicked(self):
        update_style(self.preheat_pla, "checked")
        update_style(self.preheat_abs, "unchecked")
        update_style(self.preheat_pa, "unchecked")
        update_style(self.preheat_pet, "unchecked")
        self.preheat_filament(210)

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
        self._printer.write_gcode_command('M400\nM104 S0 T0\nM104 S0 T1\nT0')
        self._printer.move_to_x(190, True)
        self.clean_handle.next_button.setEnabled(False)
        self.clean_timer.start(1900)
        self.goto_next_step_stacked_widget()
        self.clean_logo_movie.start()

    def on_clean_timer_timeout(self):
        self.clean_timer.stop()
        self.clean_handle.next_button.setEnabled(True)

    def on_clean_next_button_clicked(self):
        if self._printer.get_extruder() == "left":
            self._printer.write_gcode_command('T1')
            self._printer.move_to_x(190, True)
            self.clean_handle.next_button.setEnabled(False)
            self.clean_timer.start(4000)
        else:
            self._printer.write_gcode_command('M420 S0\nG29N\nG28\nM500\nM503\nT0\nM84')
            self.level_handle.next_button.setEnabled(False)
            self._parent.footer.setEnabled(False)
            self.clean_logo_movie.stop()
            self.goto_next_step_stacked_widget()
            self.level_mesh_graph.hide()
            self.level_load.show()
            self.level_load_timer.start(250)

    def on_level_next_button_clicked(self):
        self.offset_distance_frame.show()
        self.offset = self._printer.information['probe']['offset']
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']}({self._printer.information['probe']['offset']['left']['Z']})")
        self._printer.write_gcode_commands("G28\nT0\nG1 Y160 F8400\nG1 X190 F8400\nG1 Z0 F800")
        self.goto_next_step_stacked_widget()
        self.offset_logo_movie.start()

    @pyqtSlot(QAbstractButton)
    def on_offset_distance_button_clicked(self, button):
        if button.text() in self.offset_distance_list:
            if self.offset_button_group.id(button) != self.offset_distance_current_id:
                update_style(self.offset_button_group.button(self.offset_distance_current_id), "unchecked")
                update_style(self.offset_button_group.button(self.offset_button_group.id(button)), "checked")
                self.offset_distance_current_id = self.offset_button_group.id(button)

    def on_offset_button_up_clicked(self):
        self.offset['left']['Z'] -= float(self.offset_distance_list[self.offset_distance_current_id])
        self.offset['left']['Z'] = float('%.2f' % self.offset['left']['Z'])
        self._printer.write_gcode_command(
            'G91\nG0 F600 Z-' + self.offset_distance_list[self.offset_distance_current_id] + '\nG90')
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")

    def on_offset_button_down_clicked(self):
        self.offset['left']['Z'] += float(self.offset_distance_list[self.offset_distance_current_id])
        self.offset['left']['Z'] = float('%.2f' % self.offset['left']['Z'])
        self._printer.write_gcode_command(
            'G91\nG0 F600 Z' + self.offset_distance_list[self.offset_distance_current_id] + '\nG90')
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")

    def on_offset_next_button_clicked(self):
        self.offset_distance_frame.hide()
        self._printer.write_gcode_commands(f"M851 Z{self.offset['left']['Z']:.2f}\nM500\nM851")
        self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y160 Z150 F8400")
        self.goto_next_step_stacked_widget()
        self.offset_logo_movie.stop()
        self.place_logo_movie.start()

    def on_place_next_button_clicked(self):
        self.goto_next_step_stacked_widget()
        self.place_logo_movie.stop()
        self.measure_left_logo_movie.start()

    def on_measure_left_next_button_clicked(self):
        self._printer.write_gcode_commands(
            "G1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F320\nM400")
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(self.tr("Please enter the absolute value from the dial indicator."),
                                         "dial_indicator_left")
        self._printer.write_gcode_commands("G1 Z150 F800\nM400\nT1\nG1 X190 Z150 F8400")
        self.goto_next_step_stacked_widget()
        self.measure_left_logo_movie.stop()
        self.measure_right_logo_movie.start()

    def on_measure_right_next_button_clicked(self):
        self._printer.write_gcode_commands(
            "G1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F320\nM400")
        if not self._parent.numberPad.isVisible():
            self._parent.showShadowScreen()
            self._parent.numberPad.start(self.tr("Please enter the absolute value from the dial indicator."),
                                         "dial_indicator_right")
        self._printer.write_gcode_commands("G1 Z150 F800\nM400\nG28X")
        self.goto_next_step_stacked_widget()
        self.measure_right_logo_movie.stop()
        self.finished_handle.next_button.setText(self.tr("Done."))

    def on_finished_next_button_clicked(self):
        self._printer.save_dial_indicator_value()
        self._parent.footer.setEnabled(True)
        self._parent.gotoPreviousPage()

    def rotate_image(self, label: QLabel, image: str, angle: int):
        transform = QTransform().rotate(angle)
        rotated_image = QPixmap(image).transformed(transform, Qt.SmoothTransformation)
        label.setPixmap(rotated_image)

    def on_level_load_timer_timeout(self):
        self.level_load_rotate += 45
        if self.level_load_rotate == 360:
            self.level_load_rotate = 0
        self.rotate_image(self.level_load, "resource/icon/load.svg", self.level_load_rotate)
