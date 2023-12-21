import re

from qtCore import *
from ui.base.baseLine import BaseHLine
from ui.base.basePrintWidget import BasePrintWidget
from ui.base.basePushButton import BasePushButton
from ui.base.handleBar import HandleBar
from ui.base.messageBar import MessageBar
from ui.levelPages.levelWizardPage import LevelWizardPage

import logging
import platform

from printer import MixwareScreenPrinterStatus
from qtCore import *
from ui.base.baseLine import BaseHLine, BaseVLine
from ui.base.basePushButton import BasePushButton
from ui.base.handleBar import HandleBar
from ui.base.messageBar import MessageBar
from ui.levelPages.bedMeshGraph import BedMeshGraph


class UsePreparePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self._printer = printer
        self._parent = parent
        self.offset = {
            'left': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
            'right': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        }

        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("usePreparePage")
        self.setMinimumSize(self._printer.config.get_width(), self._printer.config.get_height() / 2)
        self.setMaximumSize(self._printer.config.get_window_size())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 20)
        self.layout.setSpacing(10)

        self.start_frame = QFrame()
        self.start_frame_layout = QVBoxLayout(self.start_frame)
        self.start_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.start_frame_layout.setSpacing(10)
        self.start_frame_layout.setAlignment(Qt.AlignCenter)
        self.start_button = BasePushButton()
        self.start_button.setFixedSize(360, 64)
        self.start_button.clicked.connect(self.on_start_button_clicked)
        self.start_frame_layout.addWidget(self.start_button)
        self.layout.addWidget(self.start_frame)

        self.message_frame = QFrame()
        self.message_frame.setObjectName("frameBox")
        self.message_frame.setFixedSize(360, 240)
        self.message_layout = QVBoxLayout(self.message_frame)
        self.message_layout.setContentsMargins(20, 20, 20, 20)
        self.message_layout.setSpacing(10)
        self.message_text_list = [
            self.tr("Clean platform debris."),
            self.tr("Place filament, select temperature"),
            self.tr("loading."),
            self.tr("Clean the nozzle."),
            self.tr("Auto bed leveling."),
            self.tr("Adjust offset."),
            self.tr("Place dial indicator."),
            self.tr("Print Verify."),
        ]
        self.message_list = []
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

        self.load_handle = HandleBar()
        self.load_handle.next_button.clicked.connect(self.on_load_next_button_clicked)
        self.load_handle_body_layout = QVBoxLayout(self.load_handle.body)
        self.load_handle_body_layout.setContentsMargins(0, 0, 0, 0)
        self.load_handle_body_layout.setSpacing(0)
        self.load_text = QLabel()
        self.load_text.setAlignment(Qt.AlignCenter)
        self.load_handle_body_layout.addWidget(self.load_text)
        self.load_progress = 0
        self.load_progress_bar = QProgressBar()
        self.load_progress_bar.setFixedHeight(18)
        self.load_handle_body_layout.addWidget(self.load_progress_bar)
        self.load_timer = QTimer()
        self.load_timer.timeout.connect(self.on_load_timer_timeout)
        self.handle_stacked_widget.addWidget(self.load_handle)

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

        self.level_handle = HandleBar()
        self.level_handle.previous_button.hide()
        self.level_handle.next_button.clicked.connect(self.on_level_next_button_clicked)
        self.level_body_layout = QVBoxLayout(self.level_handle.body)
        self.level_body_layout.setContentsMargins(20, 0, 20, 0)
        self.level_body_layout.setSpacing(0)
        self.level_body_layout.setAlignment(Qt.AlignCenter)
        self.level_button = BasePushButton()
        self.level_button.setFixedSize(120, 120)
        self.level_button.setStyleSheet("border-radius: 60px; border: 1px solid #E5E5E5")
        self.level_button.clicked.connect(self.on_level_button_clicked)
        self.level_body_layout.addWidget(self.level_button)
        self.level_load = QLabel()
        self.level_load.setFixedSize(320, 120)
        self.level_load.setAlignment(Qt.AlignCenter)
        self.level_body_layout.addWidget(self.level_load)
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
        self.offset_button_frame.setFixedHeight(168)
        self.offset_button_frame.setObjectName("frameBox")
        self.offset_button_frame_layout = QVBoxLayout(self.offset_button_frame)
        self.offset_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.offset_button_frame_layout.setSpacing(0)
        self.offset_button_up = BasePushButton()
        self.offset_button_up.setObjectName("upLogo")
        self.offset_button_up.clicked.connect(self.on_offset_button_up_clicked)
        self.offset_button_frame_layout.addWidget(self.offset_button_up)
        self.offset_button_frame_layout.addWidget(BaseHLine())
        self.offset_button_down = BasePushButton()
        self.offset_button_down.setObjectName("downLogo")
        self.offset_button_down.clicked.connect(self.on_offset_button_down_clicked)
        self.offset_button_frame_layout.addWidget(self.offset_button_down)
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
        self.place_button = BasePushButton()
        self.place_button.setFixedSize(320, 48)
        self.place_button.clicked.connect(self.on_place_button_clicked)
        self.place_body_layout.addWidget(self.place_button)
        self.handle_stacked_widget.addWidget(self.place_handle)

        self.measure_left_logo_movie = QMovie("resource/image/level_measure_left.gif")
        self.measure_left_logo_movie.setScaledSize(self.remind_logo.size())

        self.measure_right_logo_movie = QMovie("resource/image/level_measure_right.gif")
        self.measure_right_logo_movie.setScaledSize(self.remind_logo.size())

        self.work_handle = HandleBar()
        self.work_handle.previous_button.hide()
        self.work_handle.next_button.clicked.connect(self.on_work_next_button_clicked)
        self.work_body_layout = QVBoxLayout(self.work_handle.body)
        self.work_body_layout.setContentsMargins(0, 0, 0, 0)
        self.work_body_layout.setSpacing(0)
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
        self.work_text = QLabel()
        self.work_text.setWordWrap(True)
        self.work_text.setAlignment(Qt.AlignCenter)
        self.work_body_layout.addWidget(self.work_text)
        self.work_distance_frame = QFrame()
        self.work_distance_frame.setFixedHeight(128)
        self.work_distance_frame_layout = QVBoxLayout(self.work_distance_frame)
        self.work_distance_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.work_distance_frame_layout.setSpacing(0)
        self.work_distance_title = QLabel()
        self.work_distance_title.setObjectName("frame_title")
        self.work_distance_title.setFixedHeight(40)
        self.work_distance_frame_layout.addWidget(self.work_distance_title)
        self.work_distance_button_frame = QFrame()
        self.work_distance_button_frame.setObjectName("frameBox")
        self.work_distance_button_frame.setFixedHeight(88)
        self.work_distance_button_frame_layout = QHBoxLayout(self.work_distance_button_frame)
        self.work_distance_button_frame_layout.setContentsMargins(5, 1, 5, 1)
        self.work_distance_button_frame_layout.setSpacing(0)
        for d in range(len(self.offset_distance_list)):
            button = BasePushButton()
            button.setText(self.offset_distance_list[d])
            button.setObjectName("dataButton")
            self.offset_button_group.addButton(button, len(self.offset_distance_list) + d)
            if self.offset_distance_list[d] == self.offset_distance_default:
                self.on_offset_distance_button_clicked(
                    self.offset_button_group.button(len(self.offset_distance_list) + d))
            self.work_distance_button_frame_layout.addWidget(button)
        self.work_distance_frame_layout.addWidget(self.work_distance_button_frame)
        self.work_body_layout.addWidget(self.work_distance_frame)
        self.work_offset_frame = QFrame()
        self.work_offset_frame.setFixedSize(360, 210)
        self.work_offset_frame_layout = QGridLayout(self.work_offset_frame)
        self.work_offset_frame_layout.setContentsMargins(10, 0, 10, 0)
        self.work_offset_frame_layout.setSpacing(0)
        self.work_offset_x = QLabel()
        self.work_offset_x.setAlignment(Qt.AlignCenter)
        self.work_offset_frame_layout.addWidget(self.work_offset_x, 0, 0, 1, 2)
        self.work_offset_x_button = QPushButton()
        self.work_offset_x_button.setObjectName("leftLogo")
        self.work_offset_x_button.setFixedHeight(48)
        self.work_offset_x_button.clicked.connect(self.on_work_offset_x_button_clicked)
        self.work_offset_frame_layout.addWidget(self.work_offset_x_button, 0, 2, 1, 1)
        self.work_offset_x2_button = QPushButton()
        self.work_offset_x2_button.setObjectName("rightLogo")
        self.work_offset_x2_button.setFixedHeight(48)
        self.work_offset_x2_button.clicked.connect(self.on_work_offset_x2_button_clicked)
        self.work_offset_frame_layout.addWidget(self.work_offset_x2_button, 0, 3, 1, 1)
        self.work_offset_frame_layout.addWidget(BaseHLine(), 1, 0, 1, 4)
        self.work_offset_y = QLabel()
        self.work_offset_y.setAlignment(Qt.AlignCenter)
        self.work_offset_frame_layout.addWidget(self.work_offset_y, 2, 0, 1, 2)
        self.work_offset_y_button = QPushButton()
        self.work_offset_y_button.setObjectName("downLogo")
        self.work_offset_y_button.setFixedHeight(48)
        self.work_offset_y_button.clicked.connect(self.on_work_offset_y_button_clicked)
        self.work_offset_frame_layout.addWidget(self.work_offset_y_button, 2, 2, 1, 1)
        self.work_offset_y2_button = QPushButton()
        self.work_offset_y2_button.setObjectName("upLogo")
        self.work_offset_y2_button.setFixedHeight(48)
        self.work_offset_y2_button.clicked.connect(self.on_work_offset_y2_button_clicked)
        self.work_offset_frame_layout.addWidget(self.work_offset_y2_button, 2, 3, 1, 1)
        self.work_body_layout.addWidget(self.work_offset_frame)
        self.work_progress_bar = QProgressBar()
        self.work_progress_bar.setFixedHeight(18)
        self.work_body_layout.addWidget(self.work_progress_bar)
        self.handle_stacked_widget.addWidget(self.work_handle)
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
        for count in range(len(self.message_list)):
            self.message_list[count].setText(self.message_text_list[count])
            self.message_list[count].setEnabled(False)
            if count < 3:
                self.message_list[count].show()
            else:
                self.message_list[count].hide()
        self.message_list[0].setEnabled(True)
        self.message_frame.hide()
        self.start_frame.show()
        self.handle_frame.hide()
        self.handle_stacked_widget.setCurrentIndex(0)

    def re_translate_ui(self):
        self.start_button.setText(self.tr("Start"))
        self.remind_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.preheat_thermal_left_button.setText("-")
        self.preheat_thermal_right_button.setText("-")
        self.preheat_text.setText(self.tr(
            "Place consumables into the storage bin, select the corresponding temperature, and wait for heating to complete."))
        self.preheat_pla.setText("PLA")
        self.preheat_abs.setText("ABS")
        self.preheat_pet.setText("PET")
        self.preheat_pa.setText("PA")
        self.load_text.setText(self.tr("Loading filament."))
        self.clean_text.setText(self.tr("Please use a metal brush to clean the nozzle residue."))
        self.level_button.setText(self.tr("Start level"))
        self.level_text.setText(self.tr("Auto bed leveling, please wait."))
        self.offset_text.setText(self.tr("Adjust offset."))
        self.offset_distance_title.setText(self.tr("Move Distance (mm)"))
        self.offset_button_title.setText("Z: -")
        self.place_text.setText(self.tr("Place the dial indicator at the specified location."))
        self.place_button.setText(self.tr("Placed"))
        self.work_text.setText(self.tr("Verification model printing, please wait."))
        self.work_distance_title.setText(self.tr("Move Distance (mm)"))
        self.work_offset_x.setText("X: 0.0")
        self.work_offset_y.setText("Y: 0.0")

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, state):
        if state == MixwareScreenPrinterStatus.PRINTER_G29:
            logging.debug(f"Auto bed leveling completed.")
            self.level_handle.next_button.setEnabled(True)
            self.level_text.setText(self.tr("Auto bed leveling completed."))
            self.level_load_timer.stop()
            self.level_load.hide()
        elif state == MixwareScreenPrinterStatus.PRINTER_VERITY:
            self.work_thermal_frame.hide()
            self.work_progress_bar.hide()
            self.work_distance_frame.show()
            self.work_offset_frame.show()
            self.work_text.setText(
                "Printing is completed, please level the XY offset according to the printing situation.")
            self.work_handle.next_button.setEnabled(True)

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
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170:
                logging.debug(f"heat completed.")
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))

    @pyqtSlot()
    def on_start_button_clicked(self):
        self._parent.next_button.setText(self.tr("Next"))
        self._parent.next_button.setEnabled(False)
        self.start_frame.hide()
        self.message_frame.show()
        self.handle_frame.show()

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
        logging.debug(f"Start preheat")
        if platform.system().lower() == 'linux':
            self.preheat_handle.next_button.setEnabled(False)
        self.preheat_handle.next_button.setEnabled(False)  # test
        self.goto_next_step_stacked_widget()
        # preheat -> 170
        self._printer.set_thermal('left', 210)
        self._printer.set_thermal('right', 210)
        self._printer.set_thermal('bed', 60)
        self._printer.write_gcode_commands("M155 S1\nG28\nT0\nG1 Y20 Z50 F8400\nM155 S0")

    def reset_preheat_handle_ui(self):
        if self.preheat_handle.next_button.isEnabled():
            # self.preheat_text.setText(self.tr("Preheating extruder.\n(Default 170°C)"))
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
        timer_frame = 2
        self._printer.write_gcode_command(f"G91\nG0\nG1 E{load_length} F{load_speed}\nG90\nM400")
        self._printer.write_gcode_command(f"T1\nG91\nG0\nG1 E{load_length} F{load_speed}\nG90\nM400\nT0")
        self.load_progress_bar.setMaximum(int((load_time * 2 + 1) * timer_frame))
        self.working_progress = 0
        self.load_timer.start(int(1000 / timer_frame))
        self.load_handle.previous_button.hide()
        self.load_handle.next_button.setEnabled(False)  # test
        self.goto_next_step_stacked_widget()

    def on_load_timer_timeout(self):
        self.load_progress += 1
        self.load_progress_bar.setValue(self.load_progress)
        if self.handle_stacked_widget.currentWidget() == self.load_handle:
            if self.load_progress_bar.value() >= self.load_progress_bar.maximum():
                self.load_text.setText(self.tr("Filament loading completed."))
                self.load_timer.stop()
                self.load_progress_bar.hide()
                self.load_handle.next_button.setEnabled(True)
                # self.goto_next_step_stacked_widget()
                # self.load_progress_bar.setValue(0)

    def on_load_next_button_clicked(self):
        self.goto_next_step_stacked_widget()
        self.load_progress_bar.setValue(0)

    def on_clean_next_button_clicked(self):
        self.level_handle.next_button.setEnabled(False)
        self.level_load.hide()
        self.level_text.hide()
        self.goto_next_step_stacked_widget()

    def on_level_button_clicked(self):
        self._printer.write_gcode_command('G28\nD28\nG29\nM500\nM503')
        self.level_button.hide()
        self.level_load.show()
        self.level_text.show()
        self.level_load_timer.start(250)

    def on_level_next_button_clicked(self):
        self.offset_distance_frame.show()
        self.offset = self._printer.information['probe']['offset']
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']}({self._printer.information['probe']['offset']['left']['Z']})")
        self._printer.write_gcode_commands("G28\nT0\nG1 Y160 F8400\nG1 X190 F8400\nG1 Z0 F600")
        self.goto_next_step_stacked_widget()

    @pyqtSlot(QAbstractButton)
    def on_offset_distance_button_clicked(self, button):
        if button.text() in self.offset_distance_list:
            if self.offset_button_group.id(button) != self.offset_distance_current_id:
                self.offset_button_group.button(self.offset_distance_current_id).setStyleSheet(uncheckedStyleSheet)
                self.offset_button_group.button(self.offset_button_group.id(button)).setStyleSheet(checkedStyleSheet)
                self.offset_distance_current_id = self.offset_button_group.id(button)

    def on_offset_button_up_clicked(self):
        self.offset['left']['Z'] -= float(self.offset_distance_list[self.offset_distance_current_id])
        self._printer.write_gcode_command(
            'G91\nG0 F600 Z-' + self.offset_distance_list[self.offset_distance_current_id] + '\nG90')
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']: .2f}({self._printer.information['probe']['offset']['left']['Z']: .2f})")

    def on_offset_button_down_clicked(self):
        self.offset['left']['Z'] += float(self.offset_distance_list[self.offset_distance_current_id])
        self._printer.write_gcode_command(
            'G91\nG0 F600 Z' + self.offset_distance_list[self.offset_distance_current_id] + '\nG90')
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']: .2f}({self._printer.information['probe']['offset']['left']['Z']: .2f})")

    def on_offset_next_button_clicked(self):
        self.offset_distance_frame.hide()
        self._printer.write_gcode_commands(f"M851 Z{self.offset['left']['Z']}\nM500\nM851")
        self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y160 Z150 F8400")
        self.goto_next_step_stacked_widget()
        self.place_logo_movie.start()
        self.place_handle.next_button.setEnabled(False)

    def on_place_next_button_clicked(self):
        self.work_distance_frame.hide()
        self.work_offset_frame.hide()
        self.work_handle.next_button.setEnabled(False)
        self._printer.print_verify()
        self.goto_next_step_stacked_widget()
        # self.place_logo_movie.stop()
        # self.measure_left_logo_movie.start()

    def on_place_button_clicked(self):
        if self.place_button.text() == self.tr("Placed"):
            self.place_logo_movie.stop()
            self.place_logo.setMovie(self.measure_left_logo_movie)
            self.measure_left_logo_movie.start()
            self.place_text.setText(self.tr("Measure compensation value(Left)."))
            self.place_button.setText(self.tr("Measure Left"))
        elif self.place_button.text() == self.tr("Measure Left"):
            self._printer.write_gcode_commands(
                "G1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F360\nM400")
            if not self._parent.numberPad.isVisible():
                self._parent.showShadowScreen()
                self._parent.numberPad.start(f"Please enter the value from the dial indicator", "dial_indicator_left")
            self._printer.write_gcode_commands(
                "G1 Z150 F960\nM400\nG28\nG1 Y160 Z150 F8400\nM400\nT1\nG1 X190 Z150 F8400")
            self.measure_left_logo_movie.stop()
            self.place_logo.setMovie(self.measure_right_logo_movie)
            self.measure_right_logo_movie.start()
            self.place_text.setText(self.tr("Measure compensation value(Right)."))
            self.place_button.setText(self.tr("Measure Right"))
        elif self.place_button.text() == self.tr("Measure Right"):
            self.measure_right_logo_movie.stop()
            self.place_text.setText(self.tr("Measurement completed.\nPlease remove the dial indicator on the hot bed."))
            self.place_logo.hide()
            self.place_button.hide()
            self._printer.write_gcode_commands(
                "G1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F600\nM400\nG1 Z135 F840\nM400\nG1 Z120 F360\nM400")
            if not self._parent.numberPad.isVisible():
                self._parent.showShadowScreen()
                self._parent.numberPad.start(f"Please enter the value from the dial indicator", "dial_indicator_right")
            self._printer.save_dial_indicator_value()
            self._printer.write_gcode_commands("G1 Z150 F960\nM400\nG28X")
            self.place_handle.next_button.setEnabled(True)

    def on_work_offset_x_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.work_offset_x.text())
        offset = float(text[0])
        offset += float(self.offset_distance_list[self.offset_distance_current_id - len(self.offset_distance_list)])
        self.work_offset_x.setText(f"X: {offset}")

    def on_work_offset_x2_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.work_offset_x.text())
        offset = float(text[0])
        offset -= float(self.offset_distance_list[self.offset_distance_current_id - len(self.offset_distance_list)])
        self.work_offset_x.setText(f"X: {offset}")

    def on_work_offset_y_button_clicked(self):
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.work_offset_y.text())
        offset = float(text[0])
        offset -= float(self.offset_distance_list[self.offset_distance_current_id - len(self.offset_distance_list)])
        self.work_offset_y.setText(f"Y: {offset}")

    def on_work_offset_y2_button_clicked(self):
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.work_offset_y.text())
        offset = float(text[0])
        offset += float(self.offset_distance_list[self.offset_distance_current_id - len(self.offset_distance_list)])
        self.work_offset_y.setText(f"Y: {offset}")

    def on_work_next_button_clicked(self):
        text = re.findall("X: (-?\\d+\\.?\\d*)", self.work_offset_x.text())
        hotend_offset_x = float(text[0])
        text = re.findall("Y: (-?\\d+\\.?\\d*)", self.work_offset_y.text())
        hotend_offset_y = float(text[0])
        self._printer.save_hotend_offset('X', self._printer.information['probe']['offset']['right']['X'] + float(
            hotend_offset_x))
        self._printer.save_hotend_offset('Y', self._printer.information['probe']['offset']['right']['Y'] + float(
            hotend_offset_y))
        self._parent.on_next_button_clicked()

    def rotate_image(self, label: QLabel, image: str, angle: int):
        transform = QTransform().rotate(angle)
        rotated_image = QPixmap(image).transformed(transform, Qt.SmoothTransformation)
        label.setPixmap(rotated_image)

    def on_level_load_timer_timeout(self):
        self.level_load_rotate += 45
        if self.level_load_rotate == 360:
            self.level_load_rotate = 0
        self.rotate_image(self.level_load, "resource/icon/load.svg", self.level_load_rotate)


class WelcomeMainPage(BasePrintWidget):
    updateTranslator = pyqtSignal(str)
    complete = pyqtSignal()

    def __init__(self, printer, parent=None):
        super().__init__(printer, parent)
        self.current_index = 0
        self._printer = printer
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)

        self.setObjectName("welcomeMainPage")
        self.footer.hide()

        self.next_button = QPushButton(self)
        self.next_button.setFixedSize(64, 42)
        self.next_button.move(self.width() - 64 - 20, 31)
        self.next_button.clicked.connect(self.on_next_button_clicked)

        self.body_frame = QFrame()
        self.body_frame_layout = QStackedLayout(self.body_frame)
        self.body_frame_layout.setContentsMargins(0, 0, 0, 0)
        # select language
        self.language_frame = QFrame()
        self.language_frame.setObjectName('languageFrame')
        self.language_frame_layout = QVBoxLayout(self.language_frame)
        self.language_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.language_frame_layout.setSpacing(10)
        self.language_frame_layout.setAlignment(Qt.AlignTop)
        self.language_e = QPushButton(self.tr("English"))
        self.language_e.setFixedHeight(64)
        self.language_e.setObjectName("checked")
        self.language_e.clicked.connect(self.on_language_e_clicked)
        self.language_frame_layout.addWidget(self.language_e)
        self.language_c = QPushButton(self.tr("Chinese"))
        self.language_c.setFixedHeight(64)
        self.language_c.setObjectName("unchecked")
        self.language_c.clicked.connect(self.on_language_c_clicked)
        self.language_frame_layout.addWidget(self.language_c)
        self.body_frame_layout.addWidget(self.language_frame)
        # wlan connect
        # self.wlan_frame = QFrame()
        # self.body_frame_layout.addWidget(self.wlan_frame)
        # load filament
        self.usePreparePage = UsePreparePage(self._printer, self)
        self.usePreparePage.setObjectName('usePreparePage')
        self.body_frame_layout.addWidget(self.usePreparePage)

        self._page_list = [
            # {"page": self.language_frame, "title": self.tr("Language")},
            # "wlan": { "page": self.wlan_frame, "title": self.tr("WLAN")},
            # {"page": self.usePreparePage, "title": self.tr("Use Prepare")},
            {"page": self.usePreparePage, "title": self.tr("Use Prepare")},
            # { "page": self.level_frame, "title": self.tr("Auto Bed Level")},
            # { "page": self.offset_frame, "title": self.tr("Probe Offsets")},
            # { "page": self.dial_frame, "title": self.tr("Dial Indicator")},
            # { "page": self.verify_frame, "title": self.tr("Print Verify")},
        ]

        self.gotoPage(self._page_list[0]['page'], self._page_list[0]['title'], False)
        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.next_button.setText(self.tr('Next'))
        pass

    @pyqtSlot()
    def on_update_printer_information(self):
        pass

    @pyqtSlot()
    def on_next_button_clicked(self):
        if self.header.title.text() == self._page_list[-1]['title']:
            self.complete.emit()
        else:
            self.goto_next_index(self.current_index + 1)

    def goto_next_index(self, next_index: int):
        self.gotoPage(self._page_list[next_index]['page'], self._page_list[next_index]['title'], False)
        if self._page_list[next_index]['page'] == self.usePreparePage:
            self.next_button.setText(self.tr("Skip"))
        self.current_index = next_index + 1

    @pyqtSlot()
    def on_language_e_clicked(self):
        if self._printer.config.get_language() == 'Chinese':
            self.updateTranslator.emit("English")
            update_style(self.language_e, "checked")
            update_style(self.language_c, "unchecked")

    @pyqtSlot()
    def on_language_c_clicked(self):
        if self._printer.config.get_language() == 'English':
            self.updateTranslator.emit("Chinese")
            update_style(self.language_e, "unchecked")
            update_style(self.language_c, "checked")


class WelcomeStartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("welcomeStartPage")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-weight: bold; font-size: 32px;")
        self.layout.addWidget(self.title)
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setPixmap(QPixmap("resource/icon/Mixware").scaledToWidth(280))
        self.logo.setFixedSize(280, 720)
        self.layout.addWidget(self.logo)
        self.start_button = QPushButton()
        self.start_button.setFixedSize(280, 48)
        self.start_button.setStyleSheet("background-color: #FF5A00")
        self.layout.addWidget(self.start_button)
        self.re_translate_ui()

    def showEvent(self, a0: QShowEvent) -> None:
        self.re_translate_ui()

    def re_translate_ui(self):
        self.title.setText(self.tr('Welcome'))
        self.start_button.setText(self.tr('Get started'))


class WelcomeWidget(QWidget):
    updateTranslator = pyqtSignal(str)
    complete = pyqtSignal()

    def __init__(self, printer, parent=None):
        super().__init__(parent)
        self._printer = printer
        self.setObjectName("welcomeWidget")
        self.layout = QStackedLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.main_page = WelcomeMainPage(printer)
        self.main_page.complete.connect(self.goto_start_page)
        self.main_page.updateTranslator.connect(self.on_update_translator)
        self.layout.addWidget(self.main_page)
        self.start_page = WelcomeStartPage()
        self.start_page.start_button.clicked.connect(self.on_start_button_clicked)
        self.layout.addWidget(self.start_page)

    def showEvent(self, a0: QShowEvent) -> None:
        self.layout.setCurrentIndex(0)

    @pyqtSlot()
    def goto_start_page(self):
        self.layout.setCurrentWidget(self.start_page)

    @pyqtSlot()
    def on_start_button_clicked(self):
        self.complete.emit()

    @pyqtSlot(str)
    def on_update_translator(self, language: str):
        self.updateTranslator.emit(language)
