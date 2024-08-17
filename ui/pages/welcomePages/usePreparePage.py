import re

from printer import MixwareScreenPrinterStatus
from ui.components.base.baseLine import BaseHLine, BaseVLine
from ui.components.base.basePushButton import BasePushButton
from ui.components.imageItem import ImageItem
from ui.components.leveling.bedMeshGraph import BedMeshGraph
from ui.components.preHeatWidget import PreHeatWidget
from ui.components.segmented import Segmented
from ui.components.thermalWidget import ThermalWidget
from ui.pages.leveling.xYProbeTargetPage import *

enabled_verity = False


class UsePreparePage(QWidget):
    def __init__(self, printer, parent):
        super().__init__()
        self.xyoc_state = None
        self.xyoc_offsets_x = None
        self.xyoc_offsets_y = None
        self._message_title_list = None
        self._printer = printer
        self._parent = parent

        self._printer.updatePrinterStatus.connect(self.on_update_printer_status)
        self._printer.updatePrinterInformation.connect(self.on_update_printer_information)
        self._printer.endstops_hit.connect(self.on_endstops_hit)

        self.offset = {
            'left': {'X': 0.0, 'Y': 0.0, 'Z': 0.0},
            'right': {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        }
        self.reset_message_title()
        self._message_list = []

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
        self.start_logo = QLabel()
        self.start_logo.setFixedSize(360, 840)
        self.start_logo.setAlignment(Qt.AlignCenter)
        self.start_logo.setPixmap(QPixmap("resource/image/hyper-x-893").scaledToWidth(360))
        self.start_frame_layout.addWidget(self.start_logo)
        self.start_button = BasePushButton()
        self.start_button.setFixedSize(360, 64)
        self.start_button.clicked.connect(self.on_start_button_clicked)
        self.start_frame_layout.addWidget(self.start_button)
        self.layout.addWidget(self.start_frame)

        self.message_frame = BaseTitleFrame()
        self._message_list = self.message_frame.set_message(self._message_title_list)
        self.layout.addWidget(self.message_frame)

        self.handle_frame = QFrame()
        self.handle_frame.setFixedWidth(360)
        self.handle_frame.setObjectName("frameBox")
        self.handle_frame_layout = QVBoxLayout(self.handle_frame)
        self.handle_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.handle_frame_layout.setSpacing(10)
        self.handle_stacked_widget = QStackedWidget()
        self.handle_stacked_widget.setContentsMargins(0, 0, 0, 0)

        self.start_tips_handle = HandleBar()
        self.start_tips_handle.previous_button.hide()
        self.start_tips_handle.next_button.clicked.connect(lambda: self.goto_next_step_stacked_widget())
        self.start_tips_body_layout = QVBoxLayout(self.start_tips_handle.body)
        self.start_tips_body_layout.setContentsMargins(20, 10, 20, 10)
        self.start_tips_text = QLabel()
        self.start_tips_text.setFixedHeight(36)
        self.start_tips_text.setWordWrap(True)
        self.start_tips_text.setAlignment(Qt.AlignCenter)
        self.start_tips_body_layout.addWidget(self.start_tips_text)
        self.start_tips_frame = QFrame()
        self.start_tips_frame_layout = QVBoxLayout(self.start_tips_frame)
        self.start_tips_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.start_tips_pei = ImageItem("resource/image/start_pei")
        self.start_tips_frame_layout.addWidget(self.start_tips_pei)
        self.start_tips_filament = ImageItem("resource/image/start_filaments")
        self.start_tips_frame_layout.addWidget(self.start_tips_filament)
        self.start_tips_brush = ImageItem("resource/image/start_brush")
        self.start_tips_frame_layout.addWidget(self.start_tips_brush)
        self.start_tips_tool_layout = QHBoxLayout()
        self.start_tips_tool_layout.setContentsMargins(0, 0, 0, 0)
        self.start_tips_dial = ImageItem("resource/image/start_dial")
        self.start_tips_tool_layout.addWidget(self.start_tips_dial)
        self.start_tips_xypoc = ImageItem("resource/image/start_xyoc")
        self.start_tips_tool_layout.addWidget(self.start_tips_xypoc)
        self.start_tips_frame_layout.addLayout(self.start_tips_tool_layout)
        self.start_tips_body_layout.addWidget(self.start_tips_frame)
        self.handle_stacked_widget.addWidget(self.start_tips_handle)

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
        self.remind_text.setFixedHeight(72)
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
        self.preheat_filament = PreHeatWidget(self._printer, self._parent, show_bed=enabled_verity)
        self.preheat_filament.preheat_changed.connect(self.reset_preheat_handle_ui)
        self.preheat_body_layout.addWidget(self.preheat_filament)
        self.preheat_logo = MovieLabel("resource/image/place_filament.gif", 320, 388)
        self.preheat_logo.setFixedSize(320, 388)
        self.preheat_body_layout.addWidget(self.preheat_logo)
        self.preheat_text = QLabel()
        self.preheat_text.setWordWrap(True)
        self.preheat_text.setAlignment(Qt.AlignCenter)
        self.preheat_body_layout.addWidget(self.preheat_text)
        self.handle_stacked_widget.addWidget(self.preheat_handle)

        self.load_handle = HandleBar()
        self.load_handle.previous_button.clicked.connect(self.on_load_previous_button_clicked)
        self.load_handle.next_button.clicked.connect(self.on_load_next_button_clicked)
        self.load_handle_body_layout = QVBoxLayout(self.load_handle.body)
        self.load_handle_body_layout.setContentsMargins(0, 0, 0, 0)
        self.load_handle_body_layout.setSpacing(0)
        self.load_content_layout = QVBoxLayout()
        self.load_content_layout.setContentsMargins(20, 0, 20, 0)
        self.load_content_layout.setAlignment(Qt.AlignCenter)
        self.load_logo = QLabel()
        self.load_logo.setFixedHeight(320)
        self.load_logo.setAlignment(Qt.AlignCenter)
        self.load_logo.setPixmap(QPixmap("resource/image/load_filament_left").scaledToWidth(320))
        self.load_content_layout.addWidget(self.load_logo)
        self.load_text = QLabel()
        self.load_text.setFixedHeight(112)
        self.load_text.setWordWrap(True)
        self.load_text.setAlignment(Qt.AlignCenter)
        self.load_content_layout.addWidget(self.load_text)
        self.load_handle_body_layout.addLayout(self.load_content_layout)
        self.load_progress = 0
        self.load_progress_bar = QProgressBar()
        self.load_progress_bar.setTextVisible(False)
        self.load_progress_bar.setFixedHeight(18)
        self.load_handle_body_layout.addWidget(self.load_progress_bar)
        self.load_timer = QTimer()
        self.load_timer.timeout.connect(self.on_load_timer_timeout)
        self.handle_stacked_widget.addWidget(self.load_handle)

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

        self.level_handle = HandleBar()
        self.level_handle.previous_button.hide()
        self.level_handle.next_button.clicked.connect(self.on_level_next_button_clicked)
        self.level_body_layout = QVBoxLayout(self.level_handle.body)
        self.level_body_layout.setContentsMargins(19, 0, 20, 0)
        self.level_body_layout.setSpacing(0)
        self.level_body_layout.setAlignment(Qt.AlignCenter)
        self.level_button = BasePushButton()
        self.level_button.setFixedSize(240, 240)
        self.level_button.setStyleSheet("border-radius: 120px; border: 3px solid #ff5a00")
        self.level_button.clicked.connect(self.on_level_button_clicked)
        self.level_body_layout.addWidget(self.level_button)
        self.level_load = MovieLabel("resource/image/loading.gif")
        self.level_load.setFixedHeight(64)
        self.level_body_layout.addWidget(self.level_load)
        self.level_text = QLabel()
        self.level_text.setWordWrap(True)
        self.level_text.setAlignment(Qt.AlignCenter)
        self.level_body_layout.addWidget(self.level_text)
        self.level_mesh_graph = BedMeshGraph()
        self.level_mesh_graph.body_frame.setFixedSize(320, 320)
        self.level_body_layout.addWidget(self.level_mesh_graph)
        self.handle_stacked_widget.addWidget(self.level_handle)

        self.offset_handle = HandleBar()
        self.offset_handle.previous_button.hide()
        self.offset_handle.next_button.clicked.connect(self.on_offset_next_button_clicked)
        self.offset_body_layout = QVBoxLayout(self.offset_handle.body)
        self.offset_body_layout.setContentsMargins(20, 0, 20, 0)
        self.offset_body_layout.setSpacing(0)
        self.offset_logo_layout = QVBoxLayout()
        self.offset_logo_layout.setAlignment(Qt.AlignCenter)
        self.offset_logo = MovieLabel("resource/image/adjust_offset.gif", 320, 320)
        self.offset_logo.setFixedSize(320, 320)
        self.offset_logo_layout.addWidget(self.offset_logo)
        self.offset_text = QLabel()
        self.offset_text.setWordWrap(True)
        self.offset_text.setAlignment(Qt.AlignCenter)
        self.offset_logo_layout.addWidget(self.offset_text)
        self.offset_body_layout.addLayout(self.offset_logo_layout)
        self.offset_distance_frame = QFrame()
        self.offset_distance_frame.setFixedHeight(128)
        self.offset_distance_frame_layout = QVBoxLayout(self.offset_distance_frame)
        self.offset_distance_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.offset_distance_frame_layout.setSpacing(0)
        self.offset_distance_title = QLabel()
        self.offset_distance_title.setObjectName("frame_title")
        self.offset_distance_title.setFixedHeight(40)
        self.offset_distance_frame_layout.addWidget(self.offset_distance_title)
        self.offset_distance = Segmented(options=[0.01, 0.05, 0.1, 0.5, 1], default_value=0.1)
        self.offset_distance.setObjectName("frameOutLine")
        self.offset_distance_frame_layout.addWidget(self.offset_distance)
        self.offset_body_layout.addWidget(self.offset_distance_frame)
        self.offset_frame_layout = QVBoxLayout()
        self.offset_frame_layout.setContentsMargins(0, 10, 0, 10)
        self.offset_frame_layout.setSpacing(0)
        self.offset_button_title = QLabel()
        self.offset_button_title.setFixedHeight(40)
        self.offset_button_title.setObjectName("frame_title")
        self.offset_frame_layout.addWidget(self.offset_button_title)
        self.offset_button_frame = QFrame()
        self.offset_button_frame.setObjectName("frameOutLine")
        self.offset_button_frame.setFixedHeight(64)
        self.offset_button_frame_layout = QHBoxLayout(self.offset_button_frame)
        self.offset_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.offset_button_frame_layout.setSpacing(0)
        self.offset_drop_button = BasePushButton()
        self.offset_drop_button.clicked.connect(self.on_offset_drop_button_clicked)
        self.offset_button_frame_layout.addWidget(self.offset_drop_button)
        self.offset_button_frame_layout.addWidget(BaseVLine())
        self.offset_lift_button = BasePushButton()
        self.offset_lift_button.clicked.connect(self.on_offset_lift_button_clicked)
        self.offset_button_frame_layout.addWidget(self.offset_lift_button)
        self.offset_frame_layout.addWidget(self.offset_button_frame)
        self.offset_body_layout.addLayout(self.offset_frame_layout)
        self.handle_stacked_widget.addWidget(self.offset_handle)

        self.dial_handle = HandleBar()
        self.dial_handle.previous_button.hide()
        self.dial_handle.next_button.clicked.connect(self.on_place_next_button_clicked)
        self.dial_body_layout = QVBoxLayout(self.dial_handle.body)
        self.dial_body_layout.setContentsMargins(20, 0, 20, 20)
        self.dial_body_layout.setSpacing(0)
        self.dial_body_layout.setAlignment(Qt.AlignCenter)
        self.dial_placeholder = QLabel()
        self.dial_body_layout.addWidget(self.dial_placeholder)
        self.dial_logo = MovieLabel("resource/image/level_measure.gif", 320, 320)
        self.dial_logo.setFixedSize(320, 320)
        self.dial_measure_left_movie = QMovie("resource/image/level_measure_left.gif")
        self.dial_measure_right_movie = QMovie("resource/image/level_measure_right.gif")
        self.remove_dial_movie = QMovie("resource/image/remove_dial.gif")
        self.dial_body_layout.addWidget(self.dial_logo)
        self.dial_text = QLabel()
        self.dial_text.setWordWrap(True)
        self.dial_text.setAlignment(Qt.AlignCenter)
        self.dial_body_layout.addWidget(self.dial_text)
        self.dial_button = BasePushButton()
        self.dial_button.setFixedSize(320, 48)
        self.dial_button.setStyleSheet("border: 1px solid #D4D4D4")
        self.dial_button.clicked.connect(self.on_place_button_clicked)
        self.dial_body_layout.addWidget(self.dial_button)
        self.handle_stacked_widget.addWidget(self.dial_handle)

        self.xyoc_handle = HandleBar()
        self.xyoc_handle.previous_button.hide()
        self.xyoc_handle.next_button.clicked.connect(self.on_xyoc_next_button_clicked)
        self.xyoc_body_layout = QVBoxLayout(self.xyoc_handle.body)
        self.xyoc_body_layout.setContentsMargins(0, 0, 0, 0)
        self.xyoc_place_frame = QFrame()
        self.xyoc_place_frame_layout = QVBoxLayout(self.xyoc_place_frame)
        self.xyoc_place_frame_layout.setContentsMargins(20, 0, 20, 20)
        self.xyoc_place_frame_layout.setSpacing(0)
        self.xyoc_place_frame_layout.setAlignment(Qt.AlignCenter)
        self.xyoc_placeholder = QLabel()
        self.xyoc_place_frame_layout.addWidget(self.xyoc_placeholder)
        self.xyoc_x_logo = QLabel()
        self.xyoc_x_logo.setFixedHeight(320)
        self.xyoc_x_logo.setAlignment(Qt.AlignCenter)
        self.xyoc_x_logo.setPixmap(QPixmap("resource/image/xyoc_x").scaledToWidth(320))
        self.xyoc_place_frame_layout.addWidget(self.xyoc_x_logo)
        self.xyoc_y_logo = QLabel()
        self.xyoc_y_logo.setFixedHeight(320)
        self.xyoc_y_logo.setAlignment(Qt.AlignCenter)
        self.xyoc_y_logo.setPixmap(QPixmap("resource/image/xyoc_y").scaledToWidth(320))
        self.xyoc_place_frame_layout.addWidget(self.xyoc_y_logo)
        self.xyoc_place_text = QLabel()
        self.xyoc_place_text.setWordWrap(True)
        self.xyoc_place_text.setAlignment(Qt.AlignCenter)
        self.xyoc_place_frame_layout.addWidget(self.xyoc_place_text)
        self.xyoc_place_button = BasePushButton()
        self.xyoc_place_button.setFixedSize(320, 48)
        self.xyoc_place_button.setStyleSheet("border: 1px solid #D4D4D4")
        self.xyoc_place_button.clicked.connect(self.on_xyoc_place_button_clicked)
        self.xyoc_place_frame_layout.addWidget(self.xyoc_place_button)
        self.xyoc_body_layout.addWidget(self.xyoc_place_frame)

        self.xyoc_work_frame = QFrame()
        self.xyoc_work_frame_layout = QVBoxLayout(self.xyoc_work_frame)
        self.xyoc_work_frame_layout.setContentsMargins(20, 0, 20, 20)
        self.xyoc_work_frame_layout.setSpacing(0)
        self.xyoc_work_frame_layout.setAlignment(Qt.AlignCenter)
        self.xyoc_start_button = BasePushButton()
        self.xyoc_start_button.setFixedSize(240, 240)
        self.xyoc_start_button.setStyleSheet("border-radius: 120px; border: 3px solid #ff5a00")
        self.xyoc_start_button.clicked.connect(self.on_xyoc_start_button_clicked)
        self.xyoc_work_frame_layout.addWidget(self.xyoc_start_button)
        self.xyoc_load_gif = MovieLabel("resource/image/loading.gif")
        self.xyoc_load_gif.setFixedHeight(64)
        self.xyoc_work_frame_layout.addWidget(self.xyoc_load_gif)
        self.xyoc_work_text = QLabel()
        self.xyoc_work_text.setWordWrap(True)
        self.xyoc_work_text.setAlignment(Qt.AlignCenter)
        self.xyoc_work_frame_layout.addWidget(self.xyoc_work_text)
        self.xyoc_end_button = BasePushButton()
        self.xyoc_end_button.setFixedSize(320, 48)
        self.xyoc_end_button.setStyleSheet("border: 1px solid #D4D4D4")
        self.xyoc_end_button.clicked.connect(self.on_xyoc_end_button_clicked)
        self.xyoc_work_frame_layout.addWidget(self.xyoc_end_button)
        self.xyoc_body_layout.addWidget(self.xyoc_work_frame)
        self.handle_stacked_widget.addWidget(self.xyoc_handle)

        self.verity_handle = HandleBar()
        self.verity_handle.previous_button.hide()
        self.verity_handle.next_button.clicked.connect(self.on_verity_next_button_clicked)
        self.verity_body_layout = QVBoxLayout(self.verity_handle.body)
        self.verity_body_layout.setContentsMargins(0, 0, 0, 0)
        self.verity_work_frame = QFrame()
        self.verity_work_frame_layout = QVBoxLayout(self.verity_work_frame)
        self.verity_work_frame_layout.setContentsMargins(20, 0, 20, 0)
        self.verity_work_frame_layout.setSpacing(0)
        self.verity_thermal = ThermalWidget(self._printer, self._parent, show_bed=True)
        self.verity_work_frame_layout.addWidget(self.verity_thermal)
        self.verity_model_logo = QLabel()
        self.verity_model_logo.setFixedHeight(320)
        self.verity_model_logo.setAlignment(Qt.AlignCenter)
        self.verity_model_logo.setPixmap(QPixmap("resource/image/xy_verity").scaledToWidth(320))
        self.verity_work_frame_layout.addWidget(self.verity_model_logo)
        self.verity_logo = MovieLabel("resource/image/verity.gif", 320, 320)
        self.verity_logo.setFixedHeight(320)
        self.verity_work_frame_layout.addWidget(self.verity_logo)
        self.verity_text = QLabel()
        self.verity_text.setWordWrap(True)
        self.verity_text.setAlignment(Qt.AlignCenter)
        self.verity_work_frame_layout.addWidget(self.verity_text)
        self.verity_baby_step_frame = QFrame()
        self.verity_baby_step_frame.setObjectName("frameOutLine")
        self.verity_baby_step_frame.setFixedHeight(64)
        self.verity_baby_step_frame_layout = QHBoxLayout(self.verity_baby_step_frame)
        self.verity_baby_step_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.verity_baby_step_frame_layout.setSpacing(0)
        self.verity_baby_step_drop_button = BasePushButton()
        self.verity_baby_step_drop_button.clicked.connect(self.on_verity_baby_step_drop_button_clicked)
        self.verity_baby_step_frame_layout.addWidget(self.verity_baby_step_drop_button)
        self.verity_baby_step_frame_layout.addWidget(BaseVLine())
        self.verity_baby_step_lift_button = BasePushButton()
        self.verity_baby_step_lift_button.clicked.connect(self.on_verity_baby_step_lift_button_clicked)
        self.verity_baby_step_frame_layout.addWidget(self.verity_baby_step_lift_button)
        self.verity_work_frame_layout.addWidget(self.verity_baby_step_frame)
        self.verity_distance_frame = QFrame()
        self.verity_distance_frame.setFixedHeight(128)
        self.verity_distance_frame_layout = QVBoxLayout(self.verity_distance_frame)
        self.verity_distance_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.verity_distance_frame_layout.setSpacing(0)
        self.verity_distance_title = QLabel()
        self.verity_distance_title.setObjectName("frame_title")
        self.verity_distance_title.setFixedHeight(40)
        self.verity_distance_frame_layout.addWidget(self.verity_distance_title)
        self.verity_distance = Segmented(options=[0.01, 0.05, 0.1, 0.5, 1], default_value=0.1)
        self.verity_distance.setObjectName("frameOutLine")
        self.verity_distance_frame_layout.addWidget(self.verity_distance)
        self.verity_work_frame_layout.addWidget(self.verity_distance_frame)
        self.verity_offset_frame = QFrame()
        self.verity_offset_frame.setFixedHeight(168)
        self.verity_offset_frame_layout = QGridLayout(self.verity_offset_frame)
        self.verity_offset_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.verity_offset_frame_layout.setSpacing(0)
        self.verity_offset_x_label = QLabel()
        self.verity_offset_x_label.setAlignment(Qt.AlignCenter)
        self.verity_offset_frame_layout.addWidget(self.verity_offset_x_label, 0, 0, 1, 2)
        self.verity_offset_x_dec_button = QPushButton()
        self.verity_offset_x_dec_button.setObjectName("leftLogo")
        self.verity_offset_x_dec_button.clicked.connect(self.on_verity_offset_x_dec_button_clicked)
        self.verity_offset_frame_layout.addWidget(self.verity_offset_x_dec_button, 0, 2, 1, 1)
        self.verity_offset_x_add_button = QPushButton()
        self.verity_offset_x_add_button.setObjectName("rightLogo")
        self.verity_offset_x_add_button.clicked.connect(self.on_verity_offset_x_add_button_clicked)
        self.verity_offset_frame_layout.addWidget(self.verity_offset_x_add_button, 0, 3, 1, 1)
        self.verity_offset_frame_layout.addWidget(BaseHLine(), 1, 0, 1, 4)
        self.verity_offset_y_label = QLabel()
        self.verity_offset_y_label.setAlignment(Qt.AlignCenter)
        self.verity_offset_frame_layout.addWidget(self.verity_offset_y_label, 2, 0, 1, 2)
        self.verity_offset_y_dec_button = QPushButton()
        self.verity_offset_y_dec_button.setObjectName("downLogo")
        self.verity_offset_y_dec_button.clicked.connect(self.on_verity_offset_y_add_button_clicked)
        self.verity_offset_frame_layout.addWidget(self.verity_offset_y_dec_button, 2, 2, 1, 1)
        self.verity_offset_y_add_button = QPushButton()
        self.verity_offset_y_add_button.setObjectName("upLogo")
        self.verity_offset_y_add_button.clicked.connect(self.on_verity_offset_y_dec_button_clicked)
        self.verity_offset_frame_layout.addWidget(self.verity_offset_y_add_button, 2, 3, 1, 1)
        self.verity_work_frame_layout.addWidget(self.verity_offset_frame)
        self.verity_body_layout.addWidget(self.verity_work_frame)
        self.verity_progress_bar = QProgressBar()
        self.verity_progress_bar.setTextVisible(False)
        self.verity_progress_bar.setFixedHeight(18)
        self.verity_body_layout.addWidget(self.verity_progress_bar)
        if enabled_verity:
            self.handle_stacked_widget.addWidget(self.verity_handle)

        self.handle_frame_layout.addWidget(self.handle_stacked_widget)
        self.layout.addWidget(self.handle_frame)

    def showEvent(self, a0: QShowEvent) -> None:
        self.reset_ui()
        self.re_translate_ui()

    def reset_message_title(self):
        self._message_title_list = [
            self.tr("Prepare tools."),
            self.tr("Clear debris from the platform."),
            self.tr("Filament preparation."),
            self.tr("Load filament."),
            self.tr("Clean the nozzle."),
            self.tr("Auto-leveling."),
            self.tr("Adjust offset."),
            self.tr("Right extruder height calibration."),
            self.tr("XY calibration."),
        ]

    def reset_ui(self):
        self.reset_message_title()
        for count in range(len(self._message_list)):
            self._message_list[count].setText(self._message_title_list[count])
            self._message_list[count].setEnabled(False)
            if count < 3:
                self._message_list[count].show()
            else:
                self._message_list[count].hide()
        self._message_list[0].setEnabled(True)
        self.message_frame.hide()
        self.start_frame.show()
        self.handle_frame.hide()
        self.handle_stacked_widget.setCurrentIndex(0)
        self.xyoc_state = ProbeTargetStatus.XYOC_STATE_CLEAN

    def re_translate_ui(self):
        self.start_button.setText(self.tr("Start"))
        self.start_tips_text.setText(self.tr("Please have the following tools ready."))
        self.start_tips_filament.set_title(self.tr("Filament"))
        self.start_tips_dial.set_title(self.tr("Dial Indicator"))
        self.start_tips_brush.set_title(self.tr("Metal Brush"))
        self.start_tips_pei.set_title(self.tr("PEI Platform"))
        self.start_tips_xypoc.set_title(self.tr("XY Calibrator"))
        self.remind_text.setText(
            self.tr("Please place the PEI platform in a standardized manner, with no debris on the platform."))
        self.preheat_text.setText(self.tr(
            "Place consumables into the storage bin, select the corresponding temperature, and wait for heating to complete."))
        self.load_text.setText(self.tr("Loading filament(Left)."))
        self.clean_handle.previous_button.setText(self.tr("Load again"))
        self.clean_text.setText(self.tr("Please use a metal brush to clean the nozzle residue."))
        self.level_button.setText(self.tr("Start Auto-leveling"))
        self.level_text.setText(self.tr("Auto-leveling, please wait."))
        self.offset_text.setText(
            self.tr("Adjust the height between the nozzle and the platform by 'Lift Bed' or 'Drop Bed' the platform."))
        self.offset_distance_title.setText(self.tr("Move Distance (mm)"))
        self.dial_text.setText(self.tr("Place the dial indicator at the specified location."))
        self.dial_button.setText(self.tr("Placed"))
        self.verity_text.setText(self.tr("Verification model printing,\nplease wait."))
        self.verity_distance_title.setText(self.tr("Move Distance (mm)"))
        self.verity_baby_step_lift_button.setText(self.tr("Lift Bed"))
        self.verity_baby_step_drop_button.setText(self.tr("Drop Bed"))
        self.offset_lift_button.setText(self.tr("Lift Bed"))
        self.offset_drop_button.setText(self.tr("Drop Bed"))
        self.xyoc_place_text.setText(
            self.tr("Please place the xy calibrator at the designated location and connect the cable."))
        self.xyoc_place_button.setText(self.tr("Placed"))
        self.xyoc_start_button.setText(self.tr("Start calibration"))
        self.xyoc_work_text.setText(self.tr("Measuring, please wait."))
        self.xyoc_end_button.setText(self.tr("Save"))

        self.offset_button_title.setText("Z: -")
        self.verity_offset_x_label.setText("X: 0.0")
        self.verity_offset_y_label.setText("Y: 0.0")

    @pyqtSlot(MixwareScreenPrinterStatus)
    def on_update_printer_status(self, state):
        if self.isVisible():
            if state == MixwareScreenPrinterStatus.PRINTER_G29:
                self.level_handle.next_button.setEnabled(True)
                self.level_mesh_graph.show_bed_mesh(self._printer.information['bedMesh'])
                self.level_mesh_graph.show()
                self.level_text.setText(self.tr("Auto-leveling completed."))
                self.level_load.hide()
            elif state == MixwareScreenPrinterStatus.PRINTER_VERITY:
                self.verity_thermal.hide()
                self.verity_progress_bar.hide()
                self.verity_model_logo.hide()
                self.verity_baby_step_frame.hide()
                self.verity_distance_frame.show()
                self.verity_offset_frame.show()
                self.verity_logo.show()
                self.verity_text.setText(self.tr(
                    "Printing is completed, please level the XY offset according to the printing situation."))
                self.verity_handle.next_button.setEnabled(True)

    @pyqtSlot()
    def on_update_printer_information(self):
        if not self.isVisible():
            return

        if self._printer.is_print_verify():
            self.verity_progress_bar.setValue(int(self._printer.print_progress() * 100))
        if self.handle_stacked_widget.currentWidget() == self.preheat_handle and not self.preheat_handle.next_button.isEnabled():
            if self._printer.get_temperature('left') + 3 >= self._printer.get_target('left') >= 170 \
                    and self._printer.get_temperature('right') + 3 >= self._printer.get_target('right') >= 170:
                self.preheat_handle.next_button.setEnabled(True)
                self.preheat_text.setText(self.tr("Heat completed."))
        if self.handle_stacked_widget.currentWidget() == self.load_handle:
            if self.tr('Left') in self.load_text.text() and self._printer.get_extruder() == 'right':
                self.load_text.setText(self.tr("Loading filament(Right)."))
                self.load_logo.setPixmap(QPixmap("resource/image/load_filament_right").scaledToWidth(350))

    @pyqtSlot()
    def on_start_button_clicked(self):
        self._parent.next_button.setText(self.tr("Next"))
        self._parent.next_button.setEnabled(False)
        self._printer.set_led_light(1)
        self.start_frame.hide()
        self.message_frame.show()
        self.handle_frame.show()

    def goto_previous_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index > 0:
            self._message_list[index].setEnabled(False)
            self._message_list[index - 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index - 1)
            if 1 < index < self.handle_stacked_widget.count():
                self._message_list[index + 1].hide()
                self._message_list[index - 2].show()

    def goto_next_step_stacked_widget(self):
        index = self.handle_stacked_widget.currentIndex()
        if index < self.handle_stacked_widget.count():
            self._message_list[index].setEnabled(False)
            self._message_list[index + 1].setEnabled(True)
            self.handle_stacked_widget.setCurrentIndex(index + 1)
            if 0 < index < (self.handle_stacked_widget.count() - 2):
                self._message_list[index - 1].hide()
                self._message_list[index + 2].show()

    def on_remind_next_button_clicked(self):
        if is_release:
            self.preheat_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        self.preheat_filament.init_filaments()
        self._printer.write_gcode_command("M155 S1\nG28\nT0\nG1 X0 Y20 Z50 F8400\nM155 S0")

    def reset_preheat_handle_ui(self):
        if self.preheat_handle.next_button.isEnabled():
            if is_release:
                self.preheat_handle.next_button.setEnabled(False)
            self.preheat_logo.show()
            self.preheat_text.setText(self.tr(
                "Place consumables into the storage bin, select the corresponding temperature, and wait for heating to complete."))

    def on_preheat_next_button_clicked(self):
        timer_frame = 2
        self._printer.write_gcode_commands(f"G1 X190 F8400\nG91\nG1 E{load_length} F{load_speed}\nG90\nM400")
        self._printer.write_gcode_commands(
            f"T1\nG1 X190 F8400\nG91\nG1 E{load_length} F{load_speed}\nG90\nM400\nT0\nM84")
        self.load_progress_bar.setMaximum(int((load_time * 2 + 5) * timer_frame))
        self.working_progress = 0
        self.load_progress = 0
        self.load_progress_bar.setValue(self.load_progress)
        self.load_timer.start(int(1000 / timer_frame))
        self.load_logo.show()
        self.load_text.setText(self.tr("Loading filament(Left)."))
        self.load_handle.previous_button.setEnabled(False)
        if is_release:
            self.load_handle.next_button.setEnabled(False)
        self.goto_next_step_stacked_widget()
        self.preheat_filament.sync_thermal()

    def on_load_timer_timeout(self):
        self.load_progress += 1
        self.load_progress_bar.setValue(self.load_progress)
        if self.handle_stacked_widget.currentWidget() == self.load_handle:
            if self.load_progress_bar.value() >= self.load_progress_bar.maximum():
                load_comple_text = self.tr("Filament loading completed.")
                if enabled_verity:
                    load_comple_text += self.tr(
                        "\nThere will be a direct printing step during the preset process."
                        # "在预设过程中会有直接打印步骤."
                    )
                load_comple_text += self.tr(
                    "\nPlease ensure that the filament has been loaded into the extruder."
                    # "请确保耗材已装入挤出机."
                )
                self.load_text.setText(load_comple_text)
                self.load_timer.stop()
                self.load_logo.hide()
                self.load_handle.previous_button.setEnabled(True)
                self.load_handle.next_button.setEnabled(True)
                self._printer.set_thermal('left', 120 if enabled_verity else 0)
                self._printer.set_thermal('right', 120 if enabled_verity else 0)

    def on_load_next_button_clicked(self):
        self._printer.write_gcode_command('T0')
        self._printer.move_to_x(190, wait=True)
        self.clean_handle.next_button.setEnabled(False)
        self.clean_timer.start(1900)
        self.goto_next_step_stacked_widget()
        self.load_progress_bar.setValue(0)

    def on_clean_timer_timeout(self):
        self.clean_timer.stop()
        self.clean_handle.next_button.setEnabled(True)

    def on_load_previous_button_clicked(self):
        self.goto_previous_step_stacked_widget()
        self.reset_preheat_handle_ui()
        if is_release:  # test
            self.preheat_handle.next_button.setEnabled(False)
        self.preheat_filament.heat_again()

    def on_clean_next_button_clicked(self):
        if is_release:
            if self._printer.get_extruder() == "left":
                self._printer.write_gcode_command('T1')
                self._printer.move_to_x(190, wait=True)
                self.clean_handle.next_button.setEnabled(False)
                self.clean_timer.start(4000)
            else:
                self._printer.write_gcode_command('T0')
                self.level_handle.next_button.setEnabled(False)
                self.level_load.hide()
                self.level_mesh_graph.hide()
                self.level_text.hide()
                self.goto_next_step_stacked_widget()
        else:  # test
            self.level_load.hide()
            self.level_mesh_graph.hide()
            self.level_text.hide()
            self.goto_next_step_stacked_widget()

    def on_level_button_clicked(self):
        self._printer.write_gcode_command('M420 S0\nG29N\nG28\nM500\nM503\nT0\nM84')
        self.level_button.hide()
        self.level_load.show()
        self.level_text.show()

    def on_level_next_button_clicked(self):
        self.offset_distance_frame.show()
        self.offset = self._printer.information['probe']['offset']
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']}({self._printer.information['probe']['offset']['left']['Z']})")
        self._printer.write_gcode_commands("G28\nT0\nG1 Y160 F8400\nG1 X190 F8400\nG1 Z0 F800")
        self.goto_next_step_stacked_widget()

    def on_offset_lift_button_clicked(self):
        self.offset['left']['Z'] -= float(self.offset_distance.value)
        self.offset['left']['Z'] = float('%.2f' % self.offset['left']['Z'])
        self._printer.write_gcode_commands(
            'G91\nG0 F600 Z-' + self.offset_distance.value + '\nG90')
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")

    def on_offset_drop_button_clicked(self):
        self.offset['left']['Z'] += float(self.offset_distance.value)
        self.offset['left']['Z'] = float('%.2f' % self.offset['left']['Z'])
        self._printer.write_gcode_commands(
            'G91\nG0 F600 Z' + self.offset_distance.value + '\nG90')
        self.offset_button_title.setText(
            f"Z: {self.offset['left']['Z']:.2f}({self._printer.information['probe']['offset']['left']['Z']:.2f})")

    def on_offset_next_button_clicked(self):
        self.offset_distance_frame.hide()
        self._printer.write_gcode_commands(f"M851 Z{self.offset['left']['Z']:.2f}\nM500\nM851")
        self._printer.write_gcode_commands("G28\nT0\nG1 X190 Y160 Z150 F8400")
        self.goto_next_step_stacked_widget()
        if is_release:
            self.dial_handle.next_button.setEnabled(False)

    def on_place_next_button_clicked(self):
        # self.verity_distance_frame.hide()
        # self.verity_offset_frame.hide()
        # self.verity_logo.hide()
        # if is_release:  # test
        #     self.verity_handle.next_button.setEnabled(False)
        # self.preheat_filament.heat_again(True)
        # self._printer.print_verify()

        self.xyoc_handle_set(axis='X', event='place')
        self.goto_next_step_stacked_widget()

    def on_place_button_clicked(self):
        if self.dial_button.text() == self.tr("Placed"):
            self.dial_logo.set_movie(self.dial_measure_left_movie)
            self.dial_text.setText(self.tr("Measure compensation value(Left)."))
            self.dial_button.setText(self.tr("Measure Left"))
        elif self.dial_button.text() == self.tr("Measure Left"):
            self._printer.write_gcode_commands(
                "G1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F480\nM400\nG1 Z135 F840\nM400\nG1 Z120 F320\nM400")
            if not self._parent.numberPad.isVisible():
                self._parent.showShadowScreen()
                self._parent.numberPad.start(self.tr("Please enter the absolute value from the dial indicator."),
                                             "dial_indicator_left")
            self._printer.write_gcode_commands(
                "G1 Z150 F800\nM400\nT1\nG1 X190 Z150 F8400")
            self.dial_logo.set_movie(self.dial_measure_right_movie)
            self.dial_text.setText(self.tr("Measure compensation value(Right)."))
            self.dial_button.setText(self.tr("Measure Right"))
        elif self.dial_button.text() == self.tr("Measure Right"):
            self.dial_text.setText(self.tr("Measurement completed.\nPlease remove the dial indicator on the hot bed."))
            self.dial_logo.set_movie(self.remove_dial_movie)
            self.dial_button.hide()
            self._printer.write_gcode_commands(
                "G1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F480\nM400\nG1 Z135 F800\nM400\nG1 Z120 F320\nM400")
            if not self._parent.numberPad.isVisible():
                self._parent.showShadowScreen()
                self._parent.numberPad.start(self.tr("Please enter the absolute value from the dial indicator."),
                                             "dial_indicator_right")
            self._printer.save_dial_indicator_value()
            self._printer.write_gcode_commands("G1 Z150 F800\nM400\nG28X")
            self.dial_handle.next_button.setEnabled(True)

    def on_verity_baby_step_lift_button_clicked(self):
        self._printer.baby_step_lift(0.1)

    def on_verity_baby_step_drop_button_clicked(self):
        self._printer.baby_step_drop(0.1)

    def on_verity_offset_x_dec_button_clicked(self):
        data_x = re.findall("X: (-?\\d+\\.?\\d*)", self.verity_offset_x_label.text())
        offset = float(data_x[0])
        offset += float(self.verity_distance.value)
        offset = float('%.2f' % offset)
        self.verity_offset_x_label.setText(f"X: {offset:.2f}")

    def on_verity_offset_x_add_button_clicked(self):
        data_x = re.findall("X: (-?\\d+\\.?\\d*)", self.verity_offset_x_label.text())
        offset = float(data_x[0])
        offset -= float(self.verity_distance.value)
        offset = float('%.2f' % offset)
        self.verity_offset_x_label.setText(f"X: {offset:.2f}")

    def on_verity_offset_y_dec_button_clicked(self):
        data_y = re.findall("Y: (-?\\d+\\.?\\d*)", self.verity_offset_y_label.text())
        offset = float(data_y[0])
        offset -= float(self.verity_distance.value)
        offset = float('%.2f' % offset)
        self.verity_offset_y_label.setText(f"Y: {offset:.2f}")

    def on_verity_offset_y_add_button_clicked(self):
        data_y = re.findall("Y: (-?\\d+\\.?\\d*)", self.verity_offset_y_label.text())
        offset = float(data_y[0])
        offset += float(self.verity_distance.value)
        offset = float('%.2f' % offset)
        self.verity_offset_y_label.setText(f"Y: {offset:.2f}")

    def on_verity_next_button_clicked(self):
        if not is_release and not self.verity_offset_frame.isVisible():
            self.verity_thermal.hide()
            self.verity_progress_bar.hide()
            self.verity_model_logo.hide()
            self.verity_baby_step_frame.hide()
            self.verity_distance_frame.show()
            self.verity_offset_frame.show()
            self.verity_logo.show()
            self.verity_text.setText(self.tr(
                "Printing is completed, please level the XY offset according to the printing situation."))
            self.verity_handle.next_button.setEnabled(True)
            return

        data_x = re.findall("X: (-?\\d+\\.?\\d*)", self.verity_offset_x_label.text())
        hotend_offset_x = float(data_x[0])
        data_y = re.findall("Y: (-?\\d+\\.?\\d*)", self.verity_offset_y_label.text())
        hotend_offset_y = float(data_y[0])
        self._printer.set_hotend_offset('X', self._printer.information['probe']['offset']['right']['X'] + float(
            hotend_offset_x))
        self._printer.set_hotend_offset('Y', self._printer.information['probe']['offset']['right']['Y'] + float(
            hotend_offset_y))
        self._parent.on_next_button_clicked()

    def on_xyoc_next_button_clicked(self):
        self._parent.on_next_button_clicked()

    def on_xyoc_place_button_clicked(self):
        self.xyoc_handle_set(event='ready')

    def on_xyoc_start_button_clicked(self):
        if self.xyoc_state == ProbeTargetStatus.XYOC_STATE_PLACE_X:
            self.xyoc_handle_set(axis='X', event='run')
        elif self.xyoc_state == ProbeTargetStatus.XYOC_STATE_PLACE_Y:
            self.xyoc_handle_set(axis='Y', event='run')

    def on_xyoc_end_button_clicked(self):
        if self.xyoc_state == ProbeTargetStatus.XYOC_STATE_CALCULATE:
            self.probe_target_state = ProbeTargetStatus.XYOC_STATE_SAVE
            ox = float('%.2f' % (self._printer.information['probe']['offset']['right']['X'] + self.xyoc_offsets_x))
            oy = float('%.2f' % (self._printer.information['probe']['offset']['right']['Y'] + self.xyoc_offsets_y))
            self._printer.set_hotend_offset('X', ox)
            self._printer.set_hotend_offset('Y', oy)

            a0 = self.tr("Measure completed.") + f"\n\nX: {ox}\nY: {oy}"
            self.xyoc_work_text.setText(a0)
            if is_release:  # test
                self.xyoc_end_button.hide()
                self.xyoc_handle.next_button.setEnabled(True)
        elif self.xyoc_state == ProbeTargetStatus.XYOC_STATE_ERROR:
            self._printer.set_hotend_offset('X', 385, False)
            self._printer.set_hotend_offset('Y', 0, False)
            self.xyoc_handle_set(axis='X', event='place')

    @pyqtSlot(str, float)
    def on_endstops_hit(self, axis, position):
        if axis in ['X', 'Y']:
            if self.xyoc_state == ProbeTargetStatus.XYOC_STATE_MEASURING_X:
                self.xyoc_offsets_x = float('%.2f' % position)
                self.xyoc_handle_set(axis='Y', event='place')

            elif self.xyoc_state == ProbeTargetStatus.XYOC_STATE_MEASURING_Y:
                self.xyoc_offsets_y = float('%.2f' % position)
                self.xyoc_state = ProbeTargetStatus.XYOC_STATE_CALCULATE
                self.xyoc_handle_set(event='finish')

                if abs(self.xyoc_offsets_x) > 3 or abs(self.xyoc_offsets_y) > 2:
                    self.xyoc_state = ProbeTargetStatus.XYOC_STATE_ERROR
                    self._parent.showShadowScreen()
                    ret = self._parent.message.start("Mixware Screen",
                                                     self.tr("Unusual measurement data!\nPlease recalibrate."),
                                                     buttons=QMessageBox.Yes | QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                        self._printer.set_hotend_offset('X', 385, False)
                        self._printer.set_hotend_offset('Y', 0, False)
                        self.xyoc_handle_set(axis='X', event='place')
                    else:
                        self.xyoc_work_text.setText(self.tr("Unusual measurement data!\nPlease recalibrate."))
                        self.xyoc_end_button.setText(self.tr("Recalibrate"))
                    self._parent.closeShadowScreen()
                else:
                    ox = float('%.2f' %
                               (self._printer.information['probe']['offset']['right']['X'] + self.xyoc_offsets_x))
                    oy = float('%.2f' %
                               (self._printer.information['probe']['offset']['right']['Y'] + self.xyoc_offsets_y))
                    a0 = self.tr(
                        "Measure completed.") + f"\n\nX: {ox}({self.xyoc_offsets_x})\nY: {oy}({self.xyoc_offsets_y})"
                    self.xyoc_work_text.setText(a0)
                    self.xyoc_end_button.setText(self.tr("Save"))

    def xyoc_handle_set(self, axis='X', event='place'):
        if is_release:  # test
            self.xyoc_handle.next_button.setEnabled(False)

        if event == 'place':
            self._printer.write_gcode_commands(
                F"G28\n"
                F"T0\n"
                F"G1 Z{xyoc_start_pos_z} F{xyoc_feedrate_travel_z}\n"
            )
            if axis == 'X':
                self.xyoc_y_logo.hide()
                self.xyoc_x_logo.show()
                self.xyoc_state = ProbeTargetStatus.XYOC_STATE_PLACE_X
                self._printer.write_gcode_commands(
                    F"G1 X{xyoc_start_pos_x['X']} Y{xyoc_start_pos_x['Y']} F{xyoc_feedrate_travel}\n"
                )
            elif axis == 'Y':
                self.xyoc_x_logo.hide()
                self.xyoc_y_logo.show()
                self.xyoc_state = ProbeTargetStatus.XYOC_STATE_PLACE_Y
                self._printer.write_gcode_commands(
                    F"G1 X{xyoc_start_pos_y['X']} Y{xyoc_start_pos_y['Y']} F{xyoc_feedrate_travel}\n"
                )
            self.xyoc_work_frame.hide()
            self.xyoc_place_frame.show()
        else:
            self.xyoc_start_button.hide()
            self.xyoc_load_gif.hide()
            self.xyoc_work_text.hide()
            self.xyoc_end_button.hide()
            if event == 'ready':
                self.xyoc_start_button.show()
            elif event == 'run':
                self._printer.xy_probe_target()
                if self.xyoc_state == ProbeTargetStatus.XYOC_STATE_PLACE_X:
                    self.xyoc_state = ProbeTargetStatus.XYOC_STATE_MEASURING_X
                    self._printer.write_gcode_commands(F"G429XC{xyoc_measure_count}")
                elif self.xyoc_state == ProbeTargetStatus.XYOC_STATE_PLACE_Y:
                    self.xyoc_state = ProbeTargetStatus.XYOC_STATE_MEASURING_Y
                    self._printer.write_gcode_commands(F"G429YC{xyoc_measure_count}")
                self.xyoc_load_gif.show()
                self.xyoc_work_text.show()
                self.xyoc_work_text.setText(self.tr("Measuring, please wait."))
            elif event == 'finish':
                self.xyoc_work_text.show()
                self.xyoc_end_button.show()
            self.xyoc_place_frame.hide()
            self.xyoc_work_frame.show()
